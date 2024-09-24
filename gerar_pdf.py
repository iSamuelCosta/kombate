from fpdf import FPDF
from fpdf.fonts import FontFace

class PDF(FPDF):
    def __init__(self, dt_in, dt_fin):
        super().__init__()
        self.dt_in = dt_in
        self.dt_fin = dt_fin

    def header(self):
        # Logo
        self.image('imagens/Logo_kombate.png', 75, 8, 60)
        # Arial bold 15
        self.set_font('Arial', '', 8)
        # Move to the right
        self.ln(15)
        # Title
        
        self.cell(0, 5, '232 - R. Antenor Viana Braga, Itajubá, Minas Gerais', 0, 1, 'C')
        
        self.set_font('Arial', '', 5)
        self.cell(0, 5, f'Relatório de {self.dt_in} a {self.dt_fin}', 0, 1, 'C')
        self.ln(5)
        # Line break
        

    # Page footer
    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Page number
        self.cell(0, 10, 'Página ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')
    def create_table(self, df):
        self.set_font('Arial', size = 10)
        DF=df
        DF = DF.applymap(str)
        COLUMNS = [list(DF)]  # Get list of dataframe columns
        ROWS = DF.values.tolist()  # Get list of dataframe rows
        DATA = COLUMNS + ROWS
        blue = (0, 0, 0)
        grey = (128, 128, 128)
        headings_style = FontFace(emphasis="ITALICS", color=blue, fill_color=grey,)

        with self.table(
            line_height=self.font_size*1.5,
            text_align="CENTER",
            width=190,
            headings_style=headings_style
        ) as table:
            for data_row in DATA:
                row = table.row()
                for datum in data_row:
                    row.cell(datum)


class PDF3(FPDF):
    def __init__(self, dt_in, dt_fin):
        super().__init__()
        self.dt_in = dt_in
        self.dt_fin = dt_fin

    def header(self):
        # Logo
        
        # Arial bold 15
        self.set_font('Arial', '', 15)
        self.cell(0, 5, 'Monitorização das doenças diarréicas agudas', 0, 1, 'C')
                # Move to the right
        self.set_font('Arial', '', 12)
        # Title
        self.cell(0, 5, 'Distribuição de casos por faixa etária, plano de Tratamento e Procedência', 0, 1, 'C')
        
        self.set_font('Arial', '', 8)
        self.cell(0, 5, f'Relatório da semana epidemiológica de {self.dt_in} do ano de {self.dt_fin}', 0, 1, 'C')
        self.ln(5)
        # Line break
        

    # Page footer
    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Page number
        self.cell(0, 10, 'Página ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')

    def create_table(self, df, x, y, width=60):
        original_x, original_y = self.get_x(), self.get_y()
        self.set_xy(x, y)
        self.set_font('Arial', size=10)
        df = df.applymap(str)
        
        # Calcular a largura de cada coluna
        col_widths = [width/len(df.columns)] * len(df.columns)
        
        # Desenhar cabeçalho
        self.set_fill_color(200, 200, 200)
        self.set_text_color(0, 0, 255)
        self.set_font('Arial', 'B', 8)
        for i, col in enumerate(df.columns):
            self.cell(col_widths[i], 7, str(col), 1, 0, 'C', 1)
        self.ln()
        
        # Desenhar linhas de dados
        self.set_fill_color(255, 255, 255)
        self.set_text_color(0, 0, 0)
        
        self.set_font('Arial', '', 6)
        for _, row in df.iterrows():
            y=y+7
            self.set_xy(x, y)
            
            for i, value in enumerate(row):
                self.cell(col_widths[i], 7, str(value), 1, 0, 'C')
            self.ln()
        
        # Restaurar a posição original do cursor
        self.set_xy(original_x, original_y)
    def create_table2(self, df):
        self.set_font('Arial', size = 10)
        DF=df
        DF = DF.applymap(str)
        COLUMNS = [list(DF)]  # Get list of dataframe columns
        ROWS = DF.values.tolist()  # Get list of dataframe rows
        DATA = COLUMNS + ROWS
        blue = (0, 0, 0)
        grey = (128, 128, 128)
        headings_style = FontFace(emphasis="ITALICS", color=blue, fill_color=grey,)

        with self.table(
            line_height=self.font_size*1.5,
            text_align="CENTER",
            width=190,
            headings_style=headings_style
        ) as table:
            for data_row in DATA:
                row = table.row()
                for datum in data_row:
                    row.cell(datum)









class PDF2(FPDF):
    def __init__(self):
        super().__init__()
        

    def header(self):
        # Logo
        self.image('imagens\Logo_kombate.png', 75, 8, 60)
        # Arial bold 15
        self.set_font('Arial', '', 8)
        # Move to the right
        self.ln(15)
        # Title
        

        # Line break
        

    # Page footer
    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Page number
        self.cell(0, 10, 'Página ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')
    def create_table(self, df, col_width):
        self.set_font('Arial', 'B', 12)
        
        # Cabeçalho da tabela
        header = list(df.columns)
        
        # Desenha o cabeçalho
        for col in header:
            self.cell(col_width, 10, str(col), 1, 0, 'C')
        self.ln()
        self.set_font('Arial', '', 8)
        
        # Desenha os dados
        for _, row in df.iterrows():
            for col in header:
                data = str(row[col])
                lines = self.get_string_height(data) / 4.2
                if lines > 1:  # Se houver mais de uma linha de texto
                    lines = int(lines)
                    cell_height = 5 * lines
                    self.multi_cell(col_width, 5, data, 1, 'C')
                else:
                    cell_height = 10
                    self.cell(col_width, cell_height, data, 1, 0, 'C')
            self.ln()


class PDF5(FPDF):
    def __init__(self, dt_in, dt_fin):
        super().__init__()
        self.dt_in = dt_in
        self.dt_fin = dt_fin

    def header(self):
        # Logo
        self.image('imagens/Logo_kombate.png', 75, 8, 60)
        # Arial bold 15
        self.set_font('Arial', '', 8)
        # Move to the right
        self.ln(15)
        # Title
        
        self.cell(0, 5, '232 - R. Antenor Viana Braga, Itajubá, Minas Gerais', 0, 1, 'C')
        
        self.set_font('Arial', '', 5)
        self.cell(0, 5, f'Relatório de {self.dt_in} a {self.dt_fin}', 0, 1, 'C')
        self.ln(5)
        # Line break
        

    # Page footer
    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Page number
        self.cell(0, 10, 'Página ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')
    def create_table(self, df):
        self.set_font('Arial', size = 10)
        DF=df
        DF = DF.applymap(str)
        COLUMNS = [list(DF)]  # Get list of dataframe columns
        ROWS = DF.values.tolist()  # Get list of dataframe rows
        DATA = COLUMNS + ROWS
        blue = (0, 0, 0)
        grey = (128, 128, 128)
        headings_style = FontFace(emphasis="ITALICS", color=blue, fill_color=grey,)

        with self.table(
            line_height=self.font_size*1.5,
            text_align="CENTER",
            width=190,
            headings_style=headings_style
        ) as table:
            for data_row in DATA:
                row = table.row()
                for datum in data_row:
                    row.cell(datum)
