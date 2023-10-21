import tkinter as tk
from socket import socket, AF_INET, SOCK_DGRAM, IPPROTO_UDP, SOL_SOCKET, SO_REUSEADDR, SO_BROADCAST
import time
import threading



class LightArray:
    """Use UDP broadcasts to communicate with the array"""
    def __init__(self, broadcast_addr='255.255.255.255', port=4210, num_units=180):
        self.broadcast_addr = broadcast_addr
        self.broadcast_port = port
        self.num_units = num_units

        self.broadcast_sock = socket(AF_INET, SOCK_DGRAM)  
        self.broadcast_sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.broadcast_sock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

        self.unit_brightness = [0] * self.num_units
        self.unit_track = [0] * self.num_units
        self.unit_volume = [0] * self.num_units

    def send_update(self):
        message = []
        for i in range(self.num_units):
            b = int(self.unit_brightness[i] * 0xffff)
            t = int(self.unit_track[i])
            v = int(self.unit_volume[i] * 0xffff)

            message += [
                0,  # Mode = direct
                # Brightness
                (b >> 8) & 0xff,
                b & 0xff,
                # Offset
                (t >> 8) & 0xff,
                t & 0xff,
                # Volume
                (v >> 8) & 0xff,
                v & 0xff,
                0,
            ]

        assert(len(message) % 8 == 0)
        self.broadcast_sock.sendto(bytes(message), (self.broadcast_addr, self.broadcast_port))

    def set_brightness(self, unit_idx, brightness):
        if unit_idx < 0 or unit_idx > self.num_units:
            raise Exception('Unit index invalid')

        if brightness < 0 or brightness > 1:
            raise Exception('Brightness must be between 0 and 1')

        self.unit_brightness[unit_idx] = brightness

    def set_track(self, unit_idx, track):
        if unit_idx < 0 or unit_idx > self.num_units:
            raise Exception('Unit index invalid')

        if track < 1:
            raise Exception('track must be great than 1')

        self.unit_track[unit_idx] = track
        
    def set_volume(self, unit_idx, volume):
        if unit_idx < 0 or unit_idx > self.num_units:
            raise Exception('Unit index invalid')

        if volume < 0 or volume > 1:
            raise Exception('Volume must be between 0 and 1')

        self.unit_volume[unit_idx] = volume



class LightControllerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Anchor Controller")
        
               
        self.always_on_top_var = tk.BooleanVar()  # Variable to hold the state of the toggle
        self.always_on_top_checkbutton = tk.Checkbutton(root, text="Always On Top", variable=self.always_on_top_var, command=self.toggle_always_on_top)
        self.always_on_top_checkbutton.grid(row=6, column=0, columnspan=2)
   
   
        self.output_text = tk.Text(root, height=7, width=50)  # Creating a Text widget for output
        self.output_text.grid(row=7, column=0, columnspan=2)
        self.output_text.insert(tk.END, "Output Messages:\n")
        self.last_message = ""  # Variable to store the last printed message

   
        tk.Label(root, text="Unit Number:").grid(row=0, column=0)
        tk.Label(root, text="Brightness (0-1):").grid(row=1, column=0)
        tk.Label(root, text="Track #").grid(row=2, column=0)
        tk.Label(root, text="Volume (0-1):").grid(row=3, column=0)
        
        self.unit_entry = tk.Entry(root)
        self.unit_entry.grid(row=0, column=1)
        self.unit_entry.insert(0, "0")
        
        self.brightness_entry = tk.Entry(root)
        self.brightness_entry.grid(row=1, column=1)
        self.brightness_entry.insert(0, "0.0")
        
        self.track_entry = tk.Entry(root)
        self.track_entry.grid(row=2, column=1)
        self.track_entry.insert(0, "1")
        
        self.volume_entry = tk.Entry(root)
        self.volume_entry.grid(row=3, column=1)
        self.volume_entry.insert(0, "0.0")
        
        self.start_button = tk.Button(root, text="Start Broadcasting", command=self.start_broadcasting)
        self.start_button.grid(row=4, column=0, columnspan=2)
        
        self.stop_button = tk.Button(root, text="Stop Broadcasting", command=self.stop_broadcasting)
        self.stop_button.grid(row=5, column=0, columnspan=2)
                
        self.clear_button = tk.Button(root, text="Clear Output", command=self.clear_output)
        self.clear_button.grid(row=8, column=0, columnspan=2)

        
        self.broadcasting = False
        
    def toggle_always_on_top(self):
        self.root.attributes("-topmost", self.always_on_top_var.get())  # Set the always on top attribute
    

    def start_broadcasting(self):
        self.broadcasting = True
        threading.Thread(target=self.broadcast_loop).start()

    def stop_broadcasting(self):
        self.broadcasting = False
        
    def clear_output(self):
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, "Output Messages:\n")  # Inserting the initial text back



    def print_to_gui(self, message):
        if message != self.last_message:  # Check if the new message is different from the last one
            self.output_text.insert(tk.END, message + "\n")  # Inserting messages to the Text widget
            self.output_text.yview(tk.END)  # Auto-scrolling to the end of the Text widget
            self.last_message = message  # Update the last_message variable

    def broadcast_loop(self):
        
        light_array = LightArray()  # Create an instance of LightArray
        last_unit_number = None
        last_brightness = None
        last_volume = None
        last_track = None
        
        while self.broadcasting:
            try:
                unit_number = int(self.unit_entry.get())
                brightness = float(self.brightness_entry.get())
                track = float(self.track_entry.get())
                volume = float(self.volume_entry.get())

                if not (0 <= brightness <= 1 and 0 <= volume <= 1):
                    raise ValueError("Brightness and volume must be between 0 and 1")
                
                if not (1 <= track):
                    raise ValueError("track # must be greater than 0")
                
                last_unit_number = unit_number
                last_brightness = brightness
                last_track = track
                last_volume = volume
                
                # Displaying the values being sent in the GUI
                message = f"\nSending values -> \n\nUnit: \t\t  {last_unit_number}\nBrightness: \t\t{last_brightness}\nTrack: \t\t{last_track}\nVolume: \t\t{last_volume}"
                self.print_to_gui(message)
             
            except ValueError as e:
                self.print_to_gui(f"Error: {e}")  # Redirecting error messages to the GUI
                #self.print_to_gui("Continuing with previous values.")
                
                if last_unit_number is None or last_brightness is None or last_track is None or last_volume is None:
                    self.print_to_gui("Waiting for valid input.")
                    time.sleep(1)
                    continue
    


            # Setting the brightness and volume using the last known good values
            light_array.set_brightness(last_unit_number, last_brightness)
            light_array.set_volume(last_unit_number, last_volume)
            light_array.set_track(last_unit_number, last_track)
            
            # Sending the update using the send_update method
            light_array.send_update()

            time.sleep(0.1)  # Adjust the sleep time as needed
            




if __name__ == "__main__":
    root = tk.Tk()
    app = LightControllerApp(root)
    root.mainloop()
