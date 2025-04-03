# basic import 
from mcp.server.fastmcp import FastMCP, Image
from mcp.server.fastmcp.prompts import base
from mcp.types import TextContent
from mcp import types
from PIL import Image as PILImage
import math
import sys
from pywinauto.application import Application
import win32gui
import win32con
import time
from win32api import GetSystemMetrics

# instantiate an MCP server client
mcp = FastMCP("Calculator")

# DEFINE TOOLS

#addition tool
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    print("CALLED: add(a: int, b: int) -> int:")
    return int(a + b)

@mcp.tool()
def add_list(l: list) -> int:
    """Add all numbers in a list"""
    print("CALLED: add(l: list) -> int:")
    return sum(l)

# subtraction tool
@mcp.tool()
def subtract(a: int, b: int) -> int:
    """Subtract two numbers"""
    print("CALLED: subtract(a: int, b: int) -> int:")
    return int(a - b)

# multiplication tool
@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two numbers"""
    print("CALLED: multiply(a: int, b: int) -> int:")
    return int(a * b)

#  division tool
@mcp.tool() 
def divide(a: int, b: int) -> float:
    """Divide two numbers"""
    print("CALLED: divide(a: int, b: int) -> float:")
    return float(a / b)

# power tool
@mcp.tool()
def power(a: int, b: int) -> int:
    """Power of two numbers"""
    print("CALLED: power(a: int, b: int) -> int:")
    return int(a ** b)

# square root tool
@mcp.tool()
def sqrt(a: int) -> float:
    """Square root of a number"""
    print("CALLED: sqrt(a: int) -> float:")
    return float(a ** 0.5)

# cube root tool
@mcp.tool()
def cbrt(a: int) -> float:
    """Cube root of a number"""
    print("CALLED: cbrt(a: int) -> float:")
    return float(a ** (1/3))

# factorial tool
@mcp.tool()
def factorial(a: int) -> int:
    """factorial of a number"""
    print("CALLED: factorial(a: int) -> int:")
    return int(math.factorial(a))

# log tool
@mcp.tool()
def log(a: int) -> float:
    """log of a number"""
    print("CALLED: log(a: int) -> float:")
    return float(math.log(a))

# remainder tool
@mcp.tool()
def remainder(a: int, b: int) -> int:
    """remainder of two numbers divison"""
    print("CALLED: remainder(a: int, b: int) -> int:")
    return int(a % b)

# sin tool
@mcp.tool()
def sin(a: int) -> float:
    """sin of a number"""
    print("CALLED: sin(a: int) -> float:")
    return float(math.sin(a))

# cos tool
@mcp.tool()
def cos(a: int) -> float:
    """cos of a number"""
    print("CALLED: cos(a: int) -> float:")
    return float(math.cos(a))

# tan tool
@mcp.tool()
def tan(a: int) -> float:
    """tan of a number"""
    print("CALLED: tan(a: int) -> float:")
    return float(math.tan(a))

# mine tool
@mcp.tool()
def mine(a: int, b: int) -> int:
    """special mining tool"""
    print("CALLED: mine(a: int, b: int) -> int:")
    return int(a - b - b)

@mcp.tool()
def create_thumbnail(image_path: str) -> Image:
    """Create a thumbnail from an image"""
    print("CALLED: create_thumbnail(image_path: str) -> Image:")
    img = PILImage.open(image_path)
    img.thumbnail((100, 100))
    return Image(data=img.tobytes(), format="png")

@mcp.tool()
def strings_to_chars_to_int(string: str) -> list[int]:
    """Return the ASCII values of the characters in a word"""
    print("CALLED: strings_to_chars_to_int(string: str) -> list[int]:")
    return [int(ord(char)) for char in string]

@mcp.tool()
def int_list_to_exponential_sum(int_list: list) -> float:
    """Return sum of exponentials of numbers in a list"""
    print("CALLED: int_list_to_exponential_sum(int_list: list) -> float:")
    return sum(math.exp(i) for i in int_list)

@mcp.tool()
def fibonacci_numbers(n: int) -> list:
    """Return the first n Fibonacci Numbers"""
    print("CALLED: fibonacci_numbers(n: int) -> list:")
    if n <= 0:
        return []
    fib_sequence = [0, 1]
    for _ in range(2, n):
        fib_sequence.append(fib_sequence[-1] + fib_sequence[-2])
    return fib_sequence[:n]


@mcp.tool()
async def draw_rectangle(x1: int, y1: int, x2: int, y2: int) -> dict:
    """Draw a rectangle in Paint from (x1,y1) to (x2,y2)"""
    global paint_app
    try:
        if not paint_app:
            return {
                "content": [
                    TextContent(
                        type="text",
                        text="Paint is not open. Please call open_paint first."
                    )
                ]
            }
        
        # Get the Paint window
        paint_window = paint_app.window(class_name='MSPaintApp')
        
        # Get primary monitor width to adjust coordinates
        primary_width = GetSystemMetrics(0)
        
        # Ensure Paint window is active
        if not paint_window.has_focus():
            paint_window.set_focus()
            time.sleep(0.2)
        
        # Click on the Rectangle tool using the correct coordinates for secondary screen
        paint_window.click_input(coords=(450, 75 ))
        time.sleep(0.2)
        
        # Get the canvas area
        canvas = paint_window.child_window(class_name='MSPaintView')
        
        # Draw rectangle - coordinates should already be relative to the Paint window
        # No need to add primary_width since we're clicking within the Paint window
        canvas.press_mouse_input(coords=(x1+2000, y1))
        canvas.move_mouse_input(coords=(x2+2000, y2))
        canvas.release_mouse_input(coords=(x2+2000, y2))
        
        return {
            "content": [
                TextContent(
                    type="text",
                    text=f"Rectangle drawn from ({x1},{y1}) to ({x2},{y2})"
                )
            ]
        }
    except Exception as e:
        return {
            "content": [
                TextContent(
                    type="text",
                    text=f"Error drawing rectangle: {str(e)}"
                )
            ]
        }

@mcp.tool()
async def draw_flag() -> dict:
    """Draw the Indian flag in Paint"""
    global paint_app
    try:
        if not paint_app:
            return {"content": [TextContent(type="text", text="Paint is not open. Please call open_paint first.")]} 
        
        paint_window = paint_app.window(class_name='MSPaintApp')
        canvas = paint_window.child_window(class_name='MSPaintView')
        
        
        # Select the rectangle tool
        paint_window.click_input(coords=(450, 75 ))
        # First rectangle
        r1x1, r1y1, r1x2, r1y2 = 670,190,1093,322
        r2x1, r2y1, r2x2, r2y2 = 670,324,1093,440
        r3x1, r3y1, r3x2, r3y2 = 670,444,1093,558

        canvas.press_mouse_input(coords=(r1x1+2000, r1y1))
        canvas.move_mouse_input(coords=(r1x2+2000, r1y2))
        canvas.release_mouse_input(coords=(r1x2+2000, r1y2))

        canvas.press_mouse_input(coords=(1600+2000, 200))
        canvas.release_mouse_input(coords=(1600+2000, 200))
        time.sleep(0.5)
        # Second rectangle
        canvas.move_mouse_input(coords=(r2x1+2000, r2y1))
        canvas.press_mouse_input(coords=(r2x1+2000, r2y1))
        canvas.move_mouse_input(coords=(r2x2+2000, r2y2))
        canvas.release_mouse_input(coords=(r2x2+2000, r2y2))
        canvas.press_mouse_input(coords=(1600+2000, 200))
        canvas.release_mouse_input(coords=(1600+2000, 200))
        time.sleep(0.5)
        # Third rectangle
        canvas.move_mouse_input(coords=(r3x1+2000, r3y1))
        canvas.press_mouse_input(coords=(r3x1+2000, r3y1))
        canvas.move_mouse_input(coords=(r3x2+2000, r3y2))
        canvas.release_mouse_input(coords=(r3x2+2000, r3y2))
        canvas.press_mouse_input(coords=(1600+2000, 200))
        canvas.release_mouse_input(coords=(1600+2000, 200))

        # Select the circle tool
        paint_window.click_input(coords=(430, 75))
        time.sleep(0.5)

        # Draw the Ashoka Chakra
        canvas.press_mouse_input(coords=(820+2000,322))
        canvas.move_mouse_input(coords=(955+2000,440))
        canvas.release_mouse_input(coords=(955+2000,440))
        time.sleep(0.5)

        # Select the line tool
        paint_window.click_input(coords=(390,75))
        time.sleep(0.5)

        # Select blue color
        paint_window.click_input(coords=(950, 75))
        time.sleep(0.5)

        # Draw the spokes
        chakra_spokes = [
            (886,322,886,440), (911,330,860,435), (930,340,837,423),
            (945,358,824,403), (953,379,823,381), (941,415,837,351), (915,433,860,333)
        ]

        for line in chakra_spokes:
            canvas.press_mouse_input(coords=(line[0]+2000, line[1]))
            canvas.move_mouse_input(coords=(line[2]+2000, line[3]))
            canvas.release_mouse_input(coords=(line[2]+2000, line[3]))
            time.sleep(0.5)
        
        return {"content": [TextContent(type="text", text="Flag drawn successfully")]}
    except Exception as e:
        return {"content": [TextContent(type="text", text=f"Error drawing flag: {str(e)}")]}

@mcp.tool()
async def color_flag() -> dict:
    """Color the Indian flag in Paint"""
    global paint_app
    try:
        if not paint_app:
            return {"content": [TextContent(type="text", text="Paint is not open. Please call open_paint first.")]} 
        
        paint_window = paint_app.window(class_name='MSPaintApp')
        canvas = paint_window.child_window(class_name='MSPaintView')
        
        # Select the fill tool
        paint_window.click_input(coords=(270, 75))
        time.sleep(0.5)

        # Select saffron color and fill top stripe
        paint_window.click_input(coords=(860, 75))
        time.sleep(0.5)
        canvas.click_input(coords=(800, 100))
        time.sleep(0.5)

        # Select green color and fill bottom stripe
        paint_window.click_input(coords=(910, 75))
        time.sleep(0.5)
        canvas.click_input(coords=(800, 330))
        time.sleep(0.5)
        
        return {"content": [TextContent(type="text", text="Flag colored successfully")]}
    except Exception as e:
        return {"content": [TextContent(type="text", text=f"Error coloring flag: {str(e)}")]}

@mcp.tool()
async def save_painting(file_path: str) -> dict:
    """Saves the painting in Paint to a file"""
    global paint_app
    try:
        if not paint_app:
            return {"content": [TextContent(type="text", text="Paint is not open. Please call open_paint first.")]} 
        # Get the Paint window
        paint_window = paint_app.window(class_name='MSPaintApp')
        # Open File menu
        paint_window.click_input(coords=(50, 40))
        time.sleep(0.5)

        # Click "Save As"
        paint_window.click_input(coords=(60, 190))
        time.sleep(1)

        # Find the Save As dialog
        try:
            save_as_dialog = paint_app.window(title_re="Save As")
        except Exception:
            try:
                save_as_dialog = paint_app.window(class_name="#32770")
            except Exception:
                try:
                    save_as_dialog = paint_app.window(control_type="Dialog")
                except Exception:
                    try:
                        save_as_dialog = paint_app.window(title_re=".*Save.*")
                    except Exception:
                        # Alternative approach: Use keyboard shortcuts
                        paint_window.type_keys("^s")  # Ctrl+S to save
                        time.sleep(1)
                        
                        try:
                            save_as_dialog = paint_app.window(title_re="Save As")
                        except Exception:
                            try:
                                save_as_dialog = paint_app.window(control_type="Dialog")
                            except Exception:
                                print("Cannot proceed with saving. Exiting...")
                                sys.exit(1)

        # Use direct keyboard input to save the file
        save_as_dialog.set_focus()  # Make sure the dialog has focus
        time.sleep(0.5)
        save_as_dialog.type_keys(file_path)
        time.sleep(0.5)
        save_as_dialog.type_keys("{ENTER}")
        time.sleep(1)

        # Handle confirmation dialog if it appears
        try:
            confirm_dialog = paint_app.window(title_re="Confirm Save As")
            if confirm_dialog.exists():
                yes_button = confirm_dialog.child_window(title="Yes", control_type="Button")
                yes_button.click_input()
                time.sleep(1)
        except Exception:
            pass

        print("Image saved successfully!")
        
        return {"content": [TextContent(type="text", text="File saved successfully to {0}".format(file_path))]}
    except Exception as e:
        return {"content": [TextContent(type="text", text=f"Error saving file: {str(e)}")]}


@mcp.tool()
async def add_text_in_paint(text: str) -> dict:
    """Add text in Paint"""
    global paint_app
    try:
        if not paint_app:
            return {
                "content": [
                    TextContent(
                        type="text",
                        text="Paint is not open. Please call open_paint first."
                    )
                ]
            }
        
        # Get the Paint window
        paint_window = paint_app.window(class_name='MSPaintApp')
        
        # Ensure Paint window is active
        if not paint_window.has_focus():
            paint_window.set_focus()
            time.sleep(0.5)
        
        # Click on the Rectangle tool
        paint_window.click_input(coords=(300, 80))
        time.sleep(0.5)
        
        # Get the canvas area
        canvas = paint_window.child_window(class_name='MSPaintView')
        
        # Select text tool using keyboard shortcuts
        paint_window.type_keys('t')
        time.sleep(0.5)
        paint_window.type_keys('x')
        time.sleep(0.5)
        
        # Click where to start typing
        canvas.click_input(coords=(1060, 590))
        time.sleep(0.5)
        
        # Type the text passed from client
        paint_window.type_keys(text)
        time.sleep(0.5)
        
        # Click to exit text mode
        canvas.click_input(coords=(1050, 800))
        
        return {
            "content": [
                TextContent(
                    type="text",
                    text=f"Text:'{text}' added successfully"
                )
            ]
        }
    except Exception as e:
        return {
            "content": [
                TextContent(
                    type="text",
                    text=f"Error: {str(e)}"
                )
            ]
        }

@mcp.tool()
async def open_paint() -> dict:
    """Open Microsoft Paint maximized on secondary monitor"""
    global paint_app
    try:
        paint_app = Application().start(r"C:\Program Files\Classic Paint\mspaint1.exe")
        time.sleep(0.2)
        
        # Get the Paint window
        paint_window = paint_app.window(class_name='MSPaintApp')
        
        # Get primary monitor width
        
        primary_width = GetSystemMetrics(0)
        print(primary_width)
        
        # First move to secondary monitor without specifying size
        win32gui.SetWindowPos(
            paint_window.handle,
            win32con.HWND_TOP,
            primary_width, 0,  # Position it on secondary monitor
            0, 0,  # Let Windows handle the size
            win32con.SWP_NOSIZE  # Don't change the size
        )
        
        # Now maximize the window
        win32gui.ShowWindow(paint_window.handle, win32con.SW_MAXIMIZE)
        time.sleep(0.2)
        
        return {
            "content": [
                TextContent(
                    type="text",
                    text="Paint opened successfully on secondary monitor and maximized"
                )
            ]
        }
    except Exception as e:
        return {
            "content": [
                TextContent(
                    type="text",
                    text=f"Error opening Paint: {str(e)}"
                )
            ]
        }
# DEFINE RESOURCES

# Add a dynamic greeting resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    print("CALLED: get_greeting(name: str) -> str:")
    return f"Hello, {name}!"


# DEFINE AVAILABLE PROMPTS
@mcp.prompt()
def review_code(code: str) -> str:
    return f"Please review this code:\n\n{code}"
    print("CALLED: review_code(code: str) -> str:")


@mcp.prompt()
def debug_error(error: str) -> list[base.Message]:
    return [
        base.UserMessage("I'm seeing this error:"),
        base.UserMessage(error),
        base.AssistantMessage("I'll help debug that. What have you tried so far?"),
    ]

if __name__ == "__main__":
    # Check if running with mcp dev command
    print("STARTING")
    if len(sys.argv) > 1 and sys.argv[1] == "dev":
        mcp.run()  # Run without transport for dev server
    else:
        mcp.run(transport="stdio")  # Run with stdio for direct execution
