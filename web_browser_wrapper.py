import webbrowser
import os


def open_file_in_edge(file_path, new):
    # Convert absolute file path to a URL format
    # The 'file:///' prefix indicates a local file
    # url = f"file:///{os.path.abspath(file_path)}"
    url = file_path

    # Path to the Microsoft Edge executable (typical Windows location)
    # You may need to adjust this path based on your installation
    edge_path = "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe"

    try:
        # Register Edge browser
        webbrowser.register("edge", None, webbrowser.BackgroundBrowser(edge_path))
        # Open the URL in Edge
        webbrowser.get("edge").open(url, new)
        print(f"Opened {file_path} in Microsoft Edge.")
    except Exception as e:
        print(f"Error opening file in Edge: {e}")
        # Fallback to default browser if Edge is not found or fails
        webbrowser.open(url)
