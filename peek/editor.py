import console

class Editor:
    def __init__(self):
        self.editing=False
        self.data = None
        self.cursor_row = 0
        self.cursor_col = 0
        self.top_row=0
        self.cursor_state = False
        self.cursor_buffer = ""
        self.changes = False
        
    def load_data(self, data):
        # Called at the beginning of edit to instantiate data
        data_lines = data.decode().split("\n")
        data_lines.insert(0,"")
        data_lines.insert(0,"")
        self.data_lines = data_lines
    
    def close(self):
        self.editing = False
        console.disable_raw_mode()
        combined_lines = "\n".join(self.data_lines)
        self.data = combined_lines.encode("utf-8")
    
    def draw_cursor(self, buffer_data):
        cursor_char = "█"
        line = buffer_data[self.cursor_row+1]
        line_a = line[:self.cursor_col]
        line_b = line[self.cursor_col+1:]
        buffer_data[self.cursor_row+1] = ''.join([line_a, cursor_char, line_b])
        return buffer_data
        
    def place_character_into_data(self, character, row, col):
        line = self.data_lines[row]
        line_a = line[:col]
        line_b = line[col:]
        #self.cursor_buffer = line_b[0]
        #line_b = ""+line_b[1:]
        self.data_lines[row] = ''.join([line_a, character, line_b])

    def remove_character_from_data(self, row, col, offset):
        line = self.data_lines[row]     
        line_a = line[:col+offset]        
        line_b = line[col:]
        self.data_lines[row] = ''.join([line_a, line_b])
    
        
    def get_shown_data_range(self):
        buffer_data = self.data_lines.copy()
        buffer_data = self.draw_cursor(buffer_data)
        screen_rows = self.screen_rows-1
        if len(buffer_data) <= screen_rows:            
            return buffer_data, self.cursor_row, self.cursor_col
            
        center_screen_row = int(screen_rows/2)-2 # Index of the screen row in the center
        if self.cursor_row > center_screen_row:
            return buffer_data[self.cursor_row-center_screen_row:self.cursor_row+center_screen_row], center_screen_row, self.cursor_col
        else:
            return buffer_data[:screen_rows], self.cursor_row, self.cursor_col
            
      
    def draw_screen(self):
        console.clear()
        data_to_show, cursor_row, cursor_col = self.get_shown_data_range()
        for line in data_to_show:
            print(line)
        
        col_offset = 4
        console.print_at(self.screen_rows, 5, f"row:{self.cursor_row} col:{self.cursor_col} cursor:{self.cursor_state}")
        console.move_cursor(cursor_row, self.cursor_col+col_offset) 
        
            

    
    def interpret_input(self, key):
        if key == "up":
            self.cursor_row -= 1
            if self.cursor_row <0:
                self.cursor_row = 0
                
        elif key == "down":
            self.cursor_row += 1
            if self.cursor_row > len(self.data_lines)-2:
                self.cursor_row = len(self.data_lines)-2
                
        elif key == "right":
            self.cursor_col +=1
            if self.cursor_col > len(self.data_lines[self.cursor_row]):
                self.cursor_col = len(self.data_lines[self.cursor_row])
        elif key == "left":
            self.cursor_col -=1
            if self.cursor_col < 0:
                self.cursor_col = 0
                
        elif key == "backspace":
            self.remove_character_from_data(self.cursor_row+1, self.cursor_col, -1)
            self.cursor_col -=1
            self.changes=True
            
        elif key == "enter":
            self.data_lines.insert(self.cursor_row+1,"")
            self.changes=True
            self.cursor_row += 1
        
        elif key == "home":
            self.cursor_col=0
        
        elif key == "end":
            self.cursor_col = len(self.data_lines[self.cursor_row])
        
        elif key == "delete":
            self.remove_character_from_data(self.cursor_row, self.cursor_col, 1)
            self.changes=True
            
        elif key == "page_up":
            self.cursor_row -= 20
            if self.cursor_row <0:
                self.cursor_row = 0
                
        elif key == "page_down":
            self.cursor_row += 20
            if self.cursor_row > len(self.data_lines)-2:
                self.cursor_row = len(self.data_lines)-2
            
        elif key == "ctrl+x":
            self.close()
        else:
            if key.isascii():
                self.changes=True
                self.place_character_into_data(key, self.cursor_row+1, self.cursor_col)
                self.cursor_col +=len(key)
    
    def switch_cursor_state(self):
        if self.cursor_state:
            self.cursor_state = False
        else:
            self.cursor_state = True
            
        
    def edit(self, data):
        self.editing = True
        self.load_data(data)
        console.enable_raw_mode()
        
        self.screen_rows = console.get_console_lines()
        self.draw_screen()
        while self.editing:

            self.screen_rows = console.get_console_lines()

            key = console.get_input()
            self.interpret_input(key)
            self.draw_screen()
            if key == "escape":
                console.clear()
                console.disable_raw_mode()
                self.editing=False
                self.data = "\n".join(self.data_lines)
        console.clear()
        
            
            

if __name__ == "__main__":
    editor = Editor()
    editor.edit(b"what is this\ntellmefarts")