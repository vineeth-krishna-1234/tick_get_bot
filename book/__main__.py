import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

from PIL import Image
import time
from book.find_seats import detect_adjacent_colored_circles, transform_coordinates

# Configure logging
logging.basicConfig(
    filename="logger.log",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

try:
    # Setup Chrome options
    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--window-size=1920x1080")

    # Path to ChromeDriver
    service = Service("/usr/bin/chromedriver")  # Update path as needed

    driver = webdriver.Chrome(service=service, options=chrome_options)
except Exception as e:
    logging.error("Error setting up WebDriver: %s", e)


try:
    driver.get("https://www.district.in/events/delhi-capitals-team")
    wait = WebDriverWait(driver, 20)
    driver.maximize_window()
except Exception as e:
    logging.error("Error loading the webpage: %s", e)


time.sleep(5)  # Allow page to load
try:
    # Click the first "Book tickets" button
    book_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//div[text()='Book tickets']"))
    )
    book_button.click()
    time.sleep(3)  # Allow page transition
except Exception as e:
    logging.error("Error clicking 'Book tickets' button: %s", e)

time.sleep(5)  # Allow page to load
try:
    # Find all elements matching the "Book Tickets" text
    book_buttons = driver.find_elements(By.XPATH, "//p[text()='Book Tickets']")
    for button in book_buttons:
        if (
            button.is_displayed() and button.is_enabled()
        ):  # Check if visible and clickable
            button.click()
            time.sleep(3)  # Allow page transition
            break  # Exit after clicking the first valid button
    else:
        logging.error("No visible and clickable 'Book Tickets' button found.")
except Exception as e:
    logging.error("Error clicking 'Book Tickets' button: %s", e)


time.sleep(5)  # Allow page to load

try:
    # Wait for buttons with ₹ symbol to load and click the first one
    rupee_buttons = wait.until(
        EC.presence_of_all_elements_located(
            (By.XPATH, "//button[contains(text(), '₹')]")
        )
    )
    rupee_buttons[0].click()
except Exception as e:
    logging.error("Error clicking ₹ button: %s", e)


time.sleep(2)

try:
    # Find all section labels that are not sold out and click one

    available_sections = driver.find_elements(
        By.XPATH,
        "//*[name()='svg']//*[name()='g' and contains(@class, 'section-seatmap')]",
    )
    if available_sections:
        available_sections[0].click()
    else:
        logging.error("No available sections found.")
except Exception as e:
    logging.error("Error selecting available section: %s", e)


time.sleep(4)
try:
    # Find all iframes on the page
    iframes = driver.find_elements(By.TAG_NAME, "iframe")

    # Iterate through each iframe
    for iframe in iframes:
        # Switch to the iframe
        driver.switch_to.frame(iframe)

        try:
            # Check if the <div> with id="chartContainer" exists in this iframe
            chart_container = driver.find_element(By.ID, "chartContainer")
            print("Found the chartContainer div inside the iframe!")
            break  # Stop once we find the correct iframe
        except:
            # If the element is not found, switch back to the default content
            driver.switch_to.default_content()
    else:
        # If no iframe contains the chartContainer div, raise an exception
        raise Exception("No iframe with chartContainer div found")
except Exception as e:
    logging.error("Error switching to iframe or finding chartContainer: %s", e)


time.sleep(5)

try:
    div_element = driver.find_element(By.ID, "chartContainer")

    # Use ActionChains to move to the center of the div and click
    actions = ActionChains(driver)
    actions.move_to_element(div_element).click().perform()
    actions.move_to_element(div_element).click().perform()

except:
    logging.error("Error clicking div of canvas: %s", e)

time.sleep(2)
try:

    # Wait for canvas to load
    canvas = wait.until(EC.presence_of_element_located((By.TAG_NAME, "canvas")))
    actions.move_to_element(canvas).click().perform()

    time.sleep(2)

    # Take a screenshot of the canvas
    canvas.screenshot("canvas_image.png")
    canvas_width = driver.execute_script("return arguments[0].width;", canvas)
    canvas_height = driver.execute_script("return arguments[0].height;", canvas)
    print(canvas_height, canvas_width)
    with Image.open("canvas_image.png") as img:
        resized_img = img.resize((canvas_width, canvas_height))
        resized_img.save("canvas_image.png")

except Exception as e:
    logging.error("Error taking screenshot of canvas: %s", e)

try:

    seat_coordinates, _ = detect_adjacent_colored_circles("canvas_image.png")
    image = Image.open("canvas_image.png")
    image_width, image_height = image.size
    print(image_width, image_height)
    first_seat_coordinates = seat_coordinates[0][0]
    print(first_seat_coordinates)
    # first_seat_coordinates = transform_coordinates(
    #     img_x=seat_coordinates[0][0][0],
    #     img_y=seat_coordinates[0][0][1],
    #     image_width=image_width,
    #     image_height=image_height,
    #     canvas_width=canvas_width,
    #     canvas_height=canvas_height,
    # )
    print(f"first seat coordinates {first_seat_coordinates}")
except Exception as e:
    print(e)
try:

    # Get canvas size and position
    canvas_x = canvas.location["x"]
    canvas_y = canvas.location["y"]
    canvas_width = canvas.size["width"]
    canvas_height = canvas.size["height"]

    # Target coordinate on the canvas (modify as needed)
    target_x = first_seat_coordinates[0] - 1  # Replace with the provided X coordinate
    target_y = first_seat_coordinates[1] - 1  # Replace with the provided Y coordinate

    # Initialize ActionChains
    actions = ActionChains(driver)
    actions.move_by_offset(0, 0)

    # Step 1: Check if target_x is inside the current visible canvas area
    if canvas_x <= target_x <= canvas_x + canvas_width:
        print("Target is visible. Clicking directly.")
        js_script = f"""
        var marker = document.createElement('div');
        marker.style.position = 'absolute';
        marker.style.left = '{target_x}px';
        marker.style.top = '{target_y}px';
        marker.style.width = '10px';
        marker.style.height = '10px';
        marker.style.background = 'red';
        marker.style.borderRadius = '50%';
        marker.style.zIndex = '9999';
        document.body.appendChild(marker);
        setTimeout(() => marker.remove(), 10000); // Remove marker after 2 seconds
        """
        driver.execute_script(js_script)
        actions.move_by_offset(target_x, target_y).perform()
        time.sleep(1)

        js_script = f"""
        var targetX = {target_x};
        var targetY = {target_y};

        // Create a click event at the exact coordinates
        var clickEvent = new MouseEvent('click', {{
            bubbles: true,
            cancelable: true,
            view: window,
            clientX: targetX,
            clientY: targetY
        }});

        document.dispatchEvent(clickEvent);  // Dispatch the event globally
        """
        driver.execute_script(js_script)

        # Move by the target offset and perform a right click
        # actions.move_by_offset(target_x, target_y).context_click().perform()

        # actions.move_to_element_with_offset(
        #     canvas, target_x - canvas_x, target_y - canvas_y
        # ).context_click().perform()
    else:
        print("Target is outside the view. Scrolling right until it's visible.")

        # Step 2: Click and swipe to scroll right in steps
        step_size = 300  # Adjust swipe distance per step
        max_attempts = (
            target_x - canvas_x
        ) // step_size  # Limit attempts to avoid infinite loop

        for _ in range(max_attempts):
            # Click and drag right
            actions.move_to_element_with_offset(
                canvas, 50, canvas_height // 2
            ).click_and_hold().move_by_offset(step_size, 0).release().perform()
            time.sleep(1)  # Allow the scroll to take effect

            # Recalculate the new visible area
            canvas_x = canvas.location["x"]

            # If target is now visible, click and exit loop
            if canvas_x <= target_x <= canvas_x + canvas_width:
                print("Target is now visible. Clicking.")
                # actions.move_to_element_with_offset(
                #     canvas, target_x - canvas_x, target_y - canvas_y
                # ).perform()

                actions.move_to_element_with_offset(
                    canvas, target_x - canvas_x, target_y - canvas_y
                ).click().perform()
                break
        else:
            print("Could not reach target position.")
except Exception as e:
    print(e)


time.sleep(1000 * 1000)

try:
    # Close the driver
    driver.quit()
except Exception as e:
    logging.error("Error closing the WebDriver: %s", e)
