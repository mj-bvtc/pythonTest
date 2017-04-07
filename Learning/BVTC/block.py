import common
import pandas as pd


class BlockStyle(common.Common):
    def __init__(self):
        self.style = None
        self.code = None
        self.coefficient = None
        self.df = None
        self.load_styles()
        self.row = None

    def load_styles(self):
        self.df = pd.read_csv("V:\MeshLab\_FieldSurvey\MK\Spreadsheets\BLOCK_STYLES.csv")

    def find_code(self, style):
        if self.df is not None:
            self.code = self.df.Code.values[self.df.Style.values == style]
            return self.code

    def find_style(self, style):
        if self.df is not None:
            self.row = self.df[self.df.Style.values == style]
            self.code = self.row.Code.values[0]
            self.coefficient = self.row.Coefficient.values[0]
            return self.row

    def find_styles(self, code):
        if self.df is not None:
            self.row = self.df.Style.values[self.df.Code.values == code]
            return self.row


class Block(common.Common):
    """A single unit/product of masonry"""
    def __init__(self, style, style_number):
        super().__init__()
        self.project = None
        self.status = None
        self.style = style
        self.location = None
        self.quantity = None
        self.style_number = style_number
        self.orientation = None
        self.estimating_id = None
        self.region = None
        self.ornament = None
        self.form_method = None
        self.sample = None

    @property
    def block_id(self):
        prefix = self.style.code
        suffix = str(self.style_number)
        return prefix + suffix


def main():
    bs = BlockStyle()
    bs.find_style("Ashlar")
    b = Block(bs, 5)
    print(b.block_id)

if __name__ == "__main__":
    main()
