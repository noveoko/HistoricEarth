from os import system
from os.path import exists
import logging
from pathlib import Path
from dataclasses import dataclass
from typing import List, Optional, Union
import subprocess
from enum import Enum
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class TrainingMode(Enum):
    """Supported training modes for the model."""
    CUT = "CUT"
    FastCUT = "FastCUT"
    LightCUT = "LightCUT"

@dataclass
class TrainingConfig:
    """Configuration for training parameters."""
    learning_rate: float = 0.0001
    number_of_epochs: int = 200
    training_data: Path = Path("map_to_image/")
    mode: TrainingMode = TrainingMode.CUT
    name: str = "map_to_photo_CUT"
    
class GitOperationError(Exception):
    """Exception raised for errors in Git operations."""
    pass

class DependencyInstallError(Exception):
    """Exception raised for errors during dependency installation."""
    pass

class TrainingError(Exception):
    """Exception raised for errors during model training."""
    pass

def run_command(command: Union[str, List[str]], cwd: Optional[Path] = None) -> tuple[int, str, str]:
    """
    Execute a shell command and return its output.
    
    Args:
        command: Command to execute (string or list of strings)
        cwd: Working directory for command execution
    
    Returns:
        Tuple of (return_code, stdout, stderr)
    """
    try:
        process = subprocess.Popen(
            command if isinstance(command, list) else command.split(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=cwd
        )
        stdout, stderr = process.communicate()
        return process.returncode, stdout, stderr
    except subprocess.SubprocessError as e:
        logger.error(f"Command execution failed: {e}")
        raise

def clone_repo(repo_url: str = "https://github.com/taesungp/contrastive-unpaired-translation.git",
               target_dir: str = "CUT") -> None:
    """
    Clone a Git repository.
    
    Args:
        repo_url: URL of the repository to clone
        target_dir: Target directory for cloning
    
    Raises:
        GitOperationError: If cloning fails
    """
    try:
        if Path(target_dir).exists():
            logger.info(f"Repository directory {target_dir} already exists, skipping clone")
            return
        
        logger.info(f"Cloning repository from {repo_url}")
        returncode, stdout, stderr = run_command(f"git clone {repo_url} {target_dir}")
        
        if returncode != 0:
            raise GitOperationError(f"Git clone failed: {stderr}")
        
        logger.info("Repository cloned successfully")
    except Exception as e:
        logger.error(f"Failed to clone repository: {e}")
        raise GitOperationError(f"Repository cloning failed: {str(e)}")

def install_requirements(requirements_path: Path = Path("CUT/requirements.txt")) -> None:
    """
    Install Python package requirements.
    
    Args:
        requirements_path: Path to requirements.txt file
    
    Raises:
        DependencyInstallError: If installation fails
    """
    try:
        if not requirements_path.exists():
            raise FileNotFoundError(f"Requirements file not found at {requirements_path}")
        
        logger.info("Installing requirements...")
        returncode, stdout, stderr = run_command(f"pip install -r {requirements_path}")
        
        if returncode != 0:
            raise DependencyInstallError(f"Dependency installation failed: {stderr}")
        
        logger.info("Requirements installed successfully")
    except Exception as e:
        logger.error(f"Failed to install requirements: {e}")
        raise DependencyInstallError(f"Requirements installation failed: {str(e)}")

def perform_training(config: TrainingConfig) -> None:
    """
    Perform model training with given configuration.
    
    Args:
        config: Training configuration parameters
    
    Raises:
        TrainingError: If training fails
    """
    try:
        if not exists(config.training_data):
            raise FileNotFoundError(f"Training data directory not found: {config.training_data}")
        
        script_path = Path("CUT/train.py")
        if not script_path.exists():
            raise FileNotFoundError(f"Training script not found at {script_path}")
        
        training_command = [
            sys.executable,
            str(script_path),
            "--dataroot", str(config.training_data),
            "--name", config.name,
            "--CUT_mode", config.mode.value,
            "--n_epochs", str(config.number_of_epochs),
            "--lr", str(config.learning_rate)
        ]
        
        logger.info(f"Starting training with configuration: {config}")
        returncode, stdout, stderr = run_command(training_command)
        
        if returncode != 0:
            raise TrainingError(f"Training failed: {stderr}")
        
        logger.info("Training completed successfully")
    except Exception as e:
        logger.error(f"Training failed: {e}")
        raise TrainingError(f"Training process failed: {str(e)}")

def main() -> None:
    """Main execution function."""
    try:
        # Initialize training configuration
        config = TrainingConfig(
            learning_rate=0.0001,
            number_of_epochs=200,
            training_data=Path("map_to_image/"),
            mode=TrainingMode.CUT
        )
        
        # Execute pipeline
        clone_repo()
        install_requirements()
        perform_training(config)
        
    except (GitOperationError, DependencyInstallError, TrainingError) as e:
        logger.error(f"Pipeline failed: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()