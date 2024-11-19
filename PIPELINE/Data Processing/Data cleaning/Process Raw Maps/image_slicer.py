from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple, Optional
import logging
import cv2
import numpy as np
import matplotlib.pyplot as plt
from image_slicer import Tile
import image_slicer
from PIL import Image
import numpy.typing as npt

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ImageProcessingError(Exception):
    """Custom exception for image processing errors."""
    pass

@dataclass
class HistogramEqualizationConfig:
    """Configuration for histogram equalization parameters."""
    bins: int = 256
    range_min: int = 0
    range_max: int = 256
    output_dtype: str = 'uint8'

@dataclass
class ProcessingConfig:
    """Main configuration for image processing pipeline."""
    input_path: Path
    output_path: Path
    num_tiles: int
    hist_config: HistogramEqualizationConfig = HistogramEqualizationConfig()
    save_histograms: bool = False
    histogram_output_dir: Optional[Path] = None

class ImageProcessor:
    """Class to handle image processing operations."""
    
    def __init__(self, config: ProcessingConfig):
        """
        Initialize the image processor.
        
        Args:
            config: Processing configuration parameters
        """
        self.config = config
        self._validate_config()
        
        if self.config.save_histograms and self.config.histogram_output_dir:
            self.config.histogram_output_dir.mkdir(parents=True, exist_ok=True)

    def _validate_config(self) -> None:
        """Validate the configuration parameters."""
        if not self.config.input_path.exists():
            raise ImageProcessingError(f"Input file does not exist: {self.config.input_path}")
        
        if self.config.num_tiles <= 0:
            raise ValueError("Number of tiles must be positive")
        
        if self.config.save_histograms and not self.config.histogram_output_dir:
            raise ValueError("Histogram output directory must be specified when save_histograms is True")

    @staticmethod
    def compute_histogram(
        image: npt.NDArray[np.uint8],
        bins: int,
        range_min: int,
        range_max: int
    ) -> Tuple[npt.NDArray[np.float64], npt.NDArray[np.float64]]:
        """
        Compute histogram and normalized CDF for an image.
        
        Args:
            image: Input image array
            bins: Number of histogram bins
            range_min: Minimum range value
            range_max: Maximum range value
            
        Returns:
            Tuple of (normalized CDF, histogram)
        """
        hist, _ = np.histogram(image.flatten(), bins, [range_min, range_max])
        cdf = hist.cumsum()
        
        # Normalize CDF
        cdf_normalized = cdf * hist.max() / cdf.max()
        
        return cdf_normalized, hist

    def save_histogram_plot(
        self,
        cdf_normalized: npt.NDArray[np.float64],
        hist: npt.NDArray[np.float64],
        output_path: Path
    ) -> None:
        """
        Save histogram and CDF plot.
        
        Args:
            cdf_normalized: Normalized CDF array
            hist: Histogram array
            output_path: Path to save the plot
        """
        plt.figure(figsize=(10, 6))
        plt.plot(cdf_normalized, color='g', label='CDF')
        plt.hist(hist, self.config.hist_config.bins, 
                [self.config.hist_config.range_min, self.config.hist_config.range_max], 
                color='g', label='Histogram')
        plt.xlim([self.config.hist_config.range_min, self.config.hist_config.range_max])
        plt.legend(loc='upper left')
        plt.savefig(output_path)
        plt.close()

    def equalize_histogram(self, image: npt.NDArray[np.uint8]) -> npt.NDArray[np.uint8]:
        """
        Perform histogram equalization on an image.
        
        Args:
            image: Input image array
            
        Returns:
            Equalized image array
        """
        hist, _ = np.histogram(image.flatten(), self.config.hist_config.bins,
                             [self.config.hist_config.range_min, self.config.hist_config.range_max])
        cdf = hist.cumsum()
        
        # Mask zeros
        cdf_m = np.ma.masked_equal(cdf, 0)
        
        # Normalize CDF
        cdf_o = ((cdf_m - cdf_m.min()) * 255 /
                 (cdf_m.max() - cdf_m.min()))
        
        # Fill back the masked values
        cdf = np.ma.filled(cdf_o, 0).astype(self.config.hist_config.output_dtype)
        
        return cdf[image]

    def process_tile(self, tile: Tile) -> None:
        """
        Process a single image tile.
        
        Args:
            tile: Image tile to process
        """
        try:
            # Read image
            image = cv2.imread(tile.filename, cv2.IMREAD_UNCHANGED)
            if image is None:
                raise ImageProcessingError(f"Failed to read image: {tile.filename}")

            # Compute histogram and CDF
            cdf_normalized, hist = self.compute_histogram(
                image,
                self.config.hist_config.bins,
                self.config.hist_config.range_min,
                self.config.hist_config.range_max
            )

            # Save histogram plot if configured
            if self.config.save_histograms and self.config.histogram_output_dir:
                hist_path = self.config.histogram_output_dir / f"histogram_{tile.number}.png"
                self.save_histogram_plot(cdf_normalized, hist, hist_path)

            # Perform histogram equalization
            equalized_image = self.equalize_histogram(image)

            # Save processed tile
            cv2.imwrite(tile.filename, equalized_image)
            tile.image = Image.open(tile.filename)

        except Exception as e:
            logger.error(f"Error processing tile {tile.number}: {str(e)}")
            raise ImageProcessingError(f"Failed to process tile {tile.number}: {str(e)}")

    def process_image(self) -> None:
        """
        Process the entire image by splitting into tiles, processing each tile,
        and joining them back together.
        """
        try:
            logger.info(f"Starting image processing with {self.config.num_tiles} tiles")
            
            # Slice image into tiles
            tiles = image_slicer.slice(str(self.config.input_path), self.config.num_tiles)
            
            # Process each tile
            for tile in tiles:
                logger.info(f"Processing tile {tile.number}")
                self.process_tile(tile)
            
            # Join tiles back together
            final_image = image_slicer.join(tiles)
            final_image.save(self.config.output_path)
            
            logger.info("Image processing completed successfully")
            
        except Exception as e:
            logger.error(f"Error in image processing pipeline: {str(e)}")
            raise ImageProcessingError(f"Image processing pipeline failed: {str(e)}")

def main():
    """Main execution function."""
    try:
        # Configure processing parameters
        config = ProcessingConfig(
            input_path=Path('example_images/map_ready.jpg'),
            output_path=Path('processed_image.png'),
            num_tiles=64,
            save_histograms=True,
            histogram_output_dir=Path('histogram_plots'),
            hist_config=HistogramEqualizationConfig()
        )
        
        # Initialize and run processor
        processor = ImageProcessor(config)
        processor.process_image()
        
    except Exception as e:
        logger.error(f"Processing failed: {str(e)}")
        raise

if __name__ == "__main__":
    main()