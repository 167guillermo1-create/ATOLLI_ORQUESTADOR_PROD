
import os
import sys
import time
import pyautogui
import mss
import pygetwindow as gw
import cv2
import numpy as np
import google.generativeai as genai
import json
from dotenv import load_dotenv

# Load env for Gemini Key
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", ".env"))
api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
else:
    print("WARNING: No GEMINI_API_KEY found. Vision features will be disabled.")
from datetime import datetime

class NexusOculus:
    """
    NEXUS OCULUS (Desktop Edition)
    Digital Eye for automated visual verification of the desktop application.
    """
    def __init__(self, output_dir="oculus_captures"):
        self.output_dir = os.path.abspath(output_dir)
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        
        # Configure PyAutoGUI
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.5
        
        # State
        self.target_window = None
        
    def locate_window(self, title_pattern="Nexus", retries=5):
        """
        Attempts to find the application window by title with retry logic.
        """
        print(f"Oculus scanning for window with title containing: '{title_pattern}'...")
        
        for i in range(retries):
            # Buscar en todas las ventanas visibles
            all_windows = gw.getAllTitles()
            candidates = [t for t in all_windows if title_pattern.lower() in t.lower()]
            
            if candidates:
                # Priorizar coincidencias exactas o la primera encontrada
                target_title = candidates[0]
                windows = gw.getWindowsWithTitle(target_title)
                
                if windows:
                    self.target_window = windows[0]
                    print(f"✅ Found window: '{self.target_window.title}' at {self.target_window.topleft}")
                    
                    # Bring to front
                    try:
                        if self.target_window.isMinimized:
                            self.target_window.restore()
                        self.target_window.activate()
                        time.sleep(1) # Verify activation
                        return True
                    except Exception as e:
                        print(f"⚠️ Warning activating window: {e}")
                        # A veces activa pero lanza error, asumimos éxito si la encontramos
                        return True 
            
            print(f"   Searching... ({i+1}/{retries})")
            time.sleep(2)
            
        print(f"❌ Window '{title_pattern}' not found after {retries} attempts.")
        return False

    def capture_view(self, filename_suffix="view"):
        """
        Captures a screenshot of the target window (or full screen if not found).
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{filename_suffix}.png"
        filepath = os.path.join(self.output_dir, filename)
        
        with mss.mss() as sct:
            monitor = sct.monitors[1] # Default to primary
            
            if self.target_window:
                try:
                    # Attempt window-specific capture
                    monitor = {
                        "top": self.target_window.top, 
                        "left": self.target_window.left, 
                        "width": self.target_window.width, 
                        "height": self.target_window.height
                    }
                    sct_img = sct.grab(monitor)
                except Exception as e:
                    print(f"Window capture failed ({e}), falling back to full screen.")
                    monitor = sct.monitors[1]
                    sct_img = sct.grab(monitor)
            else:
                sct_img = sct.grab(monitor)
                
            mss.tools.to_png(sct_img.rgb, sct_img.size, output=filepath)
            
        print(f"Captured: {filepath}")
        return filepath

    def get_center(self):
        if not self.target_window:
            return None
        return (
            self.target_window.left + self.target_window.width // 2,
            self.target_window.top + self.target_window.height // 2
        )

    def analyze_visual_integrity(self, image_path):
        """
        Basic analysis to check if image is not purely black/white.
        Returns True if it looks like a valid UI render.
        """
        try:
            img = cv2.imread(image_path)
            if img is None:
                return False
                
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            # Check for variance (avoid single color screens)
            variance = np.var(gray)
            is_empty = variance < 5 # Very low variance means solid color
            
            if is_empty:
                print(f"Warning: Image {image_path} seems empty/solid color (Var: {variance:.2f})")
                return False
                
            return True
        except Exception as e:
            print(f"Analysis failed: {e}")
            return False

    def match_template(self, screenshot_path, template_path, threshold=0.8):
        """
        Locates a template image within the screenshot.
        Returns (x, y, w, h) of the match or None.
        """
        try:
            img = cv2.imread(screenshot_path)
            template = cv2.imread(template_path)
            if img is None or template is None:
                print("Image or Template not found for matching.")
                return None
            
            # Convert to gray for matching
            img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            # Correction: Actually read directly as gray or convert properly
            template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

            res = cv2.matchTemplate(img_gray, template_gray, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
            
            if max_val >= threshold:
                w, h = template_gray.shape[::-1]
                print(f"Template matched with confidence {max_val:.2f} at {max_loc}")
                return (max_loc[0], max_loc[1], w, h)
            else:
                print(f"Template match failed (Confidence: {max_val:.2f})")
                return None
        except Exception as e:
            print(f"Template matching error: {e}")
            return None

    def verify_region_color(self, screenshot_path, region=None, unwanted_color=(0,0,0), tollerance=10):
        """
        Checks if a specific region (x, y, w, h) or center-crop contains mostly unwanted_color.
        """
        return True

class NexusVision:
    """
    The 'Visual Cortex' of the Digital Eye.
    Uses Gemini Vision to understand the screen content semantically.
    """
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-flash-latest') # Fast model for vision

    def analyze_ui(self, image_path, prompt):
        """Generic Vision Query with Retry"""
        max_retries = 3
        for i in range(max_retries):
            try:
                print(f"Analyzing UI (Attempt {i+1}/{max_retries}): {prompt}")
                cookie_picture = {
                    'mime_type': 'image/png',
                    'data': open(image_path, 'rb').read()
                }
                response = self.model.generate_content([prompt, cookie_picture])
                return response.text
            except Exception as e:
                if "429" in str(e):
                    print(f"Rate Limit Hit. Waiting {10 * (i+1)}s...")
                    time.sleep(10 * (i+1))
                    continue
                print(f"Vision Analysis Failed: {e}")
                return None
        return None

    def find_element_coordinates(self, image_path, element_description):
        """
        Asks Gemini for the bounding box of an element.
        Returns (x, y) center point.
        """
        prompt = f"""
        Look at this UI screenshot. Find the center coordinates of the UI element described as: '{element_description}'.
        
        Return ONLY a JSON string like this: {{"x": 100, "y": 200}}
        The coordinates must be in pixels, relative to the top-left corner of the image.
        If the element is not visible, return {{"error": "not_found"}}.
        
        IMPORTANT: Be precise.
        """
        try:
            response_text = self.analyze_ui(image_path, prompt)
            if not response_text: return None
            
            # Clean generic markdown code blocks if present
            clean_text = response_text.replace("```json", "").replace("```", "").strip()
            data = json.loads(clean_text)
            
            if "error" in data:
                print(f"Element '{element_description}' not visible.")
                return None
                
            return (int(data['x']), int(data['y']))
        except Exception as e:
            print(f"Coordinate extraction failed: {e}")
            return None

class NexusInteractor:
    """
    Handles physical interactions (clicks, keyboard) for the Desktop Eye.
    Uses 'Semantic Logic' (AI Vision) to find targets.
    """
    def __init__(self, window_manager):
        self.wm = window_manager
        self.vision = NexusVision()
        
    def click_at(self, x, y):
        """Clicks at absolute coordinates safely."""
        try:
            print(f"Clicking at ({x}, {y})")
            pyautogui.moveTo(x, y, duration=0.5)
            pyautogui.click()
            time.sleep(0.5)
            return True
        except Exception as e:
            print(f"Click failed: {e}")
            return False

    def click_relative(self, rel_x, rel_y):
        """Clicks relative to the window top-left (Legacy/Fallback)."""
        if not self.wm.target_window:
            print("No target window to click relative to.")
            return False
        
        abs_x = self.wm.target_window.left + rel_x
        abs_y = self.wm.target_window.top + rel_y
        return self.click_at(abs_x, abs_y)

    def type_text(self, text, enter=True):
        """Types text into the focused element."""
        try:
            print(f"Typing: '{text}'")
            pyautogui.write(text, interval=0.05)
            if enter:
                pyautogui.press('enter')
            time.sleep(0.5)
            return True
        except Exception as e:
            print(f"Typing failed: {e}")
            return False

    def click_element_by_vision(self, description):
        """
        Takes a fresh screenshot, asks AI for coordinates of 'description', and clicks it.
        """
        print(f"Attempting to visually locate: '{description}'...")
        
        # 1. Capture 'current_view_for_vision.png'
        screenshot_path = self.wm.capture_view("vision_query")
        if not screenshot_path: return False
        
        # 2. Ask Vision
        coords = self.vision.find_element_coordinates(screenshot_path, description)
        
        # 3. Click
        if coords:
            # Coordinates from Vision are usually local to the image.
            # But capture_view grabs the specific window region if found, or full screen.
            # If grabbing specific window, we need to add window offset if the screenshot was relative? 
            # Actually nexus_oculus.capture_view uses mss.grab(monitor). 'monitor' is usually the bounding box.
            # So the image IS the cropped window.
            # Therefore, we must add the window's top-left to get absolute screen coords.
            
            win_left = self.wm.target_window.left if self.wm.target_window else 0
            win_top = self.wm.target_window.top if self.wm.target_window else 0
            
            abs_x = win_left + coords[0]
            abs_y = win_top + coords[1]
            
            return self.click_at(abs_x, abs_y)
        else:
            print(f"Vision failed to locate '{description}'")
            return False
        
    # Legacy wrapper for compatibility if needed, or deprecate.
    def click_region(self, region_name):
        """Deprecated: Use click_element_by_vision."""
        # Mapping old names to descriptions
        descriptions = {
            "tab_brain": "The 'Brain' tab or icon in the navigation bar",
            "tab_factory": "The 'Factory' tab or icon in the navigation bar",
            "tab_matrix": "The 'Matrix' tab or icon in the navigation bar",
            "tab_config": "The 'Config' tab or icon in the navigation bar",
            "factory_input_name": "The text input field for Project Name",
            "factory_generate_btn": "The button labeled 'GENERAR PROYECTO'",
            "config_groq_input": "The input field for Groq API Key",
            "config_save_btn": "The button labeled 'GUARDAR CONFIGURACIÓN'"
        }
        
        if region_name in descriptions:
            return self.click_element_by_vision(descriptions[region_name])
        else:
            print(f"Unknown region: {region_name}")
            return False

if __name__ == "__main__":
    # Test Routine
    eye = NexusOculus()
    if eye.locate_window("NEXUS"):
        eye.capture_view("test_found")
    else:
        eye.capture_view("test_not_found")
