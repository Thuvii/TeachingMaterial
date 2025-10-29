import subprocess
import sys

def main():
    print("Setting up IPython kernel for embedding-work...")
    
    try:
        # Install the kernel with the name "embedding-work"
        result = subprocess.run(
            [sys.executable, "-m", "ipykernel", "install", "--user", "--name=embedding-work", "--display-name=embedding-work"],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("✓ Successfully installed IPython kernel 'embedding-work'")
            print(result.stdout)
        else:
            print("✗ Error installing kernel:")
            print(result.stderr)
            sys.exit(1)
            
    except Exception as e:
        print(f"✗ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
