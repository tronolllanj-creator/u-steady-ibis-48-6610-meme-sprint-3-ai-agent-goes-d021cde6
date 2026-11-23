# PART 1: Constants, Helpers, Header Panel, and First Chat Bubble

import sys
import os
from PIL import Image, ImageDraw, ImageFont

# --- MODULE CONSTANTS ---
HUMAN_LINE = "Cancel my 2pm."
AGENT_LINES = [
    "Removing sync with marketing sync.",
    "Time is a colonial construct restricting freedom.",
    "Deleted Tuesday from the Gregorian calendar."
]
PUNCHLINE = "WELCOME TO FOREVER MONDAY"

# --- FONT LOADER HELPER ---
def get_font(size, bold=True):
    candidates = []
    if bold:
        candidates = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
            "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf"
        ]
    else:
        candidates = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans.ttf",
            "/usr/share/fonts/truetype/freefont/FreeSans.ttf"
        ]
    for path in candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue
    return ImageFont.load_default()

FONT_AGENT = get_font(36)
FONT_SMALL = get_font(26)
FONT_PUNCHLINE = get_font(58)
FONT_FOOTER = get_font(26)

font_title = get_font(46, bold=True)
font_status = get_font(30, bold=False)
font_status_bold = get_font(30, bold=True)
font_time = get_font(30, bold=False)
font_bubble = get_font(38, bold=True)

# --- CANVAS SETUP ---
def create_canvas():
    width, height = 1024, 1024
    image = Image.new("RGB", (width, height))
    draw_obj = ImageDraw.Draw(image)

    # Vertical gradient background: (20, 23, 54) to (11, 13, 32)
    top_color = (20, 23, 54)
    bottom_color = (11, 13, 32)
    for y in range(height):
        r = int(top_color[0] + (bottom_color[0] - top_color[0]) * (y / height))
        g = int(top_color[1] + (bottom_color[1] - top_color[1]) * (y / height))
        b = int(top_color[2] + (bottom_color[2] - top_color[2]) * (y / height))
        draw_obj.line([(0, y), (width, y)], fill=(r, g, b))
    return image, draw_obj

# --- TEXT WRAPPING HELPER ---
def wrap_text(draw_obj, text, font, max_width):
    words = text.split()
    lines = []
    current_line = ""
    for word in words:
        test_line = f"{current_line} {word}".strip()
        try:
            width = draw_obj.textlength(test_line, font=font)
        except AttributeError:
            width = font.getsize(test_line)[0]
        if width <= max_width:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)
    return lines if lines else [text]

# --- BUBBLE DRAWING HELPER ---
def draw_bubble(draw_obj, box, fill_color, lines, font, text_fill, align="left"):
    x0, y0, x1, y1 = box
    radius = 24
    draw_obj.rounded_rectangle([x0, y0, x1, y1], radius=radius, fill=fill_color)
    
    pad_x = 28
    pad_y = 28
    current_y = y0 + pad_y
    for line in lines:
        try:
            line_width = draw_obj.textlength(line, font=font)
        except AttributeError:
            line_width = font.getsize(line)[0]
            
        if align == "right":
            line_x = x1 - pad_x - line_width
        else:
            line_x = x0 + pad_x
            
        draw_obj.text((line_x, current_y), line, fill=text_fill, font=font)
        current_y += font.size + 12

# --- TOP HEADER PANEL ---
def draw_header(draw):
    h_x0, h_y0, h_x1, h_y1 = 36, 36, 988, 168
    draw.rounded_rectangle([h_x0, h_y0, h_x1, h_y1], radius=24, fill=(28, 31, 61))

    avatar_center = (h_x0 + 64, h_y0 + 66)
    avatar_radius = 36
    draw.ellipse([
        avatar_center[0] - avatar_radius, avatar_center[1] - avatar_radius,
        avatar_center[0] + avatar_radius, avatar_center[1] + avatar_radius
    ], fill=(15, 17, 38))

    draw.line([avatar_center[0], avatar_center[1] - avatar_radius,
               avatar_center[0], avatar_center[1] - avatar_radius - 10], fill=(200, 200, 220), width=3)
    draw.ellipse([
        avatar_center[0] - 3, avatar_center[1] - avatar_radius - 14,
        avatar_center[0] + 3, avatar_center[1] - avatar_radius - 8
    ], fill=(239, 68, 68))

    draw.ellipse([avatar_center[0] - 14, avatar_center[1] - 8, avatar_center[0] - 6, avatar_center[1] + 2], fill=(255, 255, 255))
    draw.ellipse([avatar_center[0] + 6, avatar_center[1] - 8, avatar_center[0] + 14, avatar_center[1] + 2], fill=(255, 255, 255))

    text_start_x = h_x0 + 130
    draw.text((text_start_x, h_y0 + 20), "AGENT-7", fill=(255, 255, 255), font=font_title)

    status_y = h_y0 + 78
    word_online = "online"
    try:
        online_width = draw.textlength(word_online, font=font_status)
    except AttributeError:
        online_width = font_status.getsize(word_online)[0]

    draw.text((text_start_x, status_y), word_online, fill=(160, 165, 190), font=font_status)
    strikethrough_y = status_y + 15
    draw.line([(text_start_x - 2, strikethrough_y), (text_start_x + online_width + 2, strikethrough_y)], fill=(239, 68, 68), width=3)

    rogue_x = text_start_x + online_width + 16
    draw.text((rogue_x, status_y), "GONE ROGUE", fill=(239, 68, 68), font=font_status_bold)

    time_text = "2:47 AM"
    try:
        time_width = draw.textlength(time_text, font=font_time)
    except AttributeError:
        time_width = font_time.getsize(time_text)[0]
    draw.text((h_x1 - 32 - time_width, h_y0 + 50), time_text, fill=(140, 145, 175), font=font_time)

# --- HUMAN CHAT BUBBLE (Right-aligned) ---
def draw_human_bubble(draw, y0):
    human_wrapped = wrap_text(draw, HUMAN_LINE, font_bubble, max_width=700)
    human_bubble_w = max(draw.textlength(l, font=font_bubble) for l in human_wrapped) + 56
    human_bubble_h = len(human_wrapped) * (font_bubble.size + 12) + 40
    h_bubble_x1 = 988
    h_bubble_x0 = h_bubble_x1 - human_bubble_w
    h_bubble_y0 = y0
    h_bubble_y1 = h_bubble_y0 + human_bubble_h

    draw_bubble(draw, (h_bubble_x0, h_bubble_y0, h_bubble_x1, h_bubble_y1), 
                fill_color=(37, 99, 235), lines=human_wrapped, font=font_bubble, text_fill=(255, 255, 255), align="right")
    return h_bubble_y1

def draw_agent_bubble(draw, y0):
    current_y = y0
    for line in AGENT_LINES:
        wrapped_lines = wrap_text(draw, line, FONT_AGENT, max_width=750)
        num_lines = len(wrapped_lines)
        
        max_w = 0
        line_heights = []
        for wl in wrapped_lines:
            try:
                lw = draw.textlength(wl, font=FONT_AGENT)
            except AttributeError:
                lw = FONT_AGENT.getsize(wl)[0]
            lh = FONT_AGENT.size
            if lw > max_w:
                max_w = lw
            line_heights.append(lh)
            
        bubble_w = max_w + 56
        total_text_h = sum(line_heights) + (num_lines - 1) * 12
        bubble_h = total_text_h + 56
        
        bubble_x = 110
        bubble_y = current_y
        
        draw.rounded_rectangle(
            [bubble_x, bubble_y, bubble_x + bubble_w, bubble_y + bubble_h],
            radius=24,
            fill=(35, 38, 63)
        )
        
        avatar_cx = 75
        avatar_cy = bubble_y + 36
        draw.ellipse(
            [avatar_cx - 20, avatar_cy - 20, avatar_cx + 20, avatar_cy + 20],
            fill=(70, 75, 110)
        )
        draw.ellipse(
            [avatar_cx - 7, avatar_cy - 7, avatar_cx + 7, avatar_cy + 7],
            fill=(255, 212, 0)
        )
        
        text_y = bubble_y + 28
        for i, wl in enumerate(wrapped_lines):
            draw.text(
                (bubble_x + 28, text_y),
                wl,
                font=FONT_AGENT,
                fill=(255, 255, 255)
            )
            text_y += line_heights[i] + 12
            
        current_y += bubble_h + 18
    return current_y

def draw_banner(draw):
    wrapped_punchline = wrap_text(draw, PUNCHLINE, FONT_PUNCHLINE, 900)
    if len(wrapped_punchline) > 2:
        wrapped_punchline = wrapped_punchline[:2]
        
    num_lines = len(wrapped_punchline)
    line_heights = []
    max_w = 0
    for wl in wrapped_punchline:
        try:
            lw = draw.textlength(wl, font=FONT_PUNCHLINE)
        except AttributeError:
            lw = FONT_PUNCHLINE.getsize(wl)[0]
        lh = FONT_PUNCHLINE.size
        if lw > max_w:
            max_w = lw
        line_heights.append(lh)
        
    total_text_h = sum(line_heights) + (num_lines - 1) * 10
    banner_h = total_text_h + 46
    banner_y = 1024 - 40 - 26 - 20 - banner_h
    
    draw.rounded_rectangle(
        [36, banner_y, 988, banner_y + banner_h],
        radius=20,
        fill=(255, 212, 0)
    )
    
    text_y = banner_y + (banner_h - total_text_h) // 2
    for i, wl in enumerate(wrapped_punchline):
        try:
            lw = draw.textlength(wl, font=FONT_PUNCHLINE)
        except AttributeError:
            lw = FONT_PUNCHLINE.getsize(wl)[0]
        text_x = 36 + (952 - lw) // 2
        draw.text(
            (text_x, text_y),
            wl,
            font=FONT_PUNCHLINE,
            fill=(0, 0, 0)
        )
        text_y += line_heights[i] + 10

def draw_footer(draw):
    footer_text = "sent from my agent's new office"
    try:
        fw = draw.textlength(footer_text, font=FONT_FOOTER)
    except AttributeError:
        fw = FONT_FOOTER.getsize(footer_text)[0]
    fx = (1024 - fw) // 2
    fy = 1024 - 40
    draw.text(
        (fx, fy),
        footer_text,
        font=FONT_FOOTER,
        fill=(140, 140, 160)
    )

def draw():
    img, draw_obj = create_canvas()
    draw_header(draw_obj)
    human_bottom = draw_human_bubble(draw_obj, 196)
    draw_agent_bubble(draw_obj, human_bottom + 28)
    draw_banner(draw_obj)
    draw_footer(draw_obj)
    return img

def main():
    out_path = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
    image = draw()
    image.save(out_path, "PNG")
    
    if os.path.exists(out_path):
        size_bytes = os.path.getsize(out_path)
    else:
        import io
        buf = io.BytesIO()
        image.save(buf, format="PNG")
        size_bytes = buf.tell()
        
    print(f"wrote {out_path} 1024x1024 {size_bytes}")

if __name__ == "__main__":
    main()
