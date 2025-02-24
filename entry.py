import sys
import traceback

def run_main():
    try:
        from src.main import main
        return main()
    except Exception as e:
        print("Detailed error information:")
        print(f"Error type: {type(e).__name__}")
        print(f"Error message: {str(e)}")
        print("\nTraceback:")
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    try:
        sys.exit(run_main())
    except Exception as e:
        print("\nFatal error:")
        traceback.print_exc()
        sys.exit(1)
