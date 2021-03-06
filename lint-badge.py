import subprocess 
import sys
from cairosvg import svg2png
from cairosvg import svg2svg
from pybadges import badge
from rflint import RfLint
from argparse import ArgumentParser
from pathlib import Path


LOGO="data:image/png;base64,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"


FILE = "badge.html"

def main():
    
    parser = ArgumentParser()
    parser.add_argument(
        "-a",
        "--arguments",
        action="store",
        type=str,
        dest="rf_file",
        help="RFLINT Arguments"
        )
    parser.add_argument(
        "-f",
        "--format",
        action="store",
        type=str,
        dest="file_format",
        help="File format. Can be either png or svg"
        )
    
    args = parser.parse_args()
    
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
        
    rf_file = args.rf_file
    file_format = args.file_format
    create_badge(rf_file, file_format)

def create_badge(robotfile, file):

    error_count = RfLint().run(robotfile)
    if error_count > 0 and error_count < 5:
        badge_svg  = badge(left_text='RFLINT', 
                    right_text='Errors count:' + str(error_count),
                    right_color='green', logo=LOGO, embed_logo=False)
        convert_svg(badge_svg, file)
    elif error_count > 5 and error_count < 9:
        badge_svg = badge(left_text='RFLINT', 
                    right_text='Errors count:' + str(error_count),
                    right_color='yellow', logo=LOGO, embed_logo=False)
        convert_svg(badge_svg, file)
    elif error_count >= 9:
        badge_svg = badge(left_text='RFLINT', 
                    right_text='Errors count:' + str(error_count),
                    right_color='red', logo=LOGO, embed_logo=False)
        convert_svg(badge_svg, file)

def convert_svg(svg, file):
    if file == 'png':
        svg2png(bytestring=svg,write_to='badge.png')
    else:
        svg2svg(bytestring=svg,write_to='badge.svg')

if __name__ == "__main__":
    main()