import gspread
from gspread import WorksheetNotFound
from gspread.utils import rowcol_to_a1
from gspread_formatting import batch_updater, CellFormat, Color, TextFormat, NumberFormat


def check_fit(game, players):
    try:
        try:
            vote_result = next(item['result'] for item in game['suggested_numplayers'] if item['numplayers'] == str(players) or '+' in item['numplayers'])
        except Exception as e:
            print("Problem with players vote result:")
            print(game)
            return "Unknown"
        best = next(int(result['numvotes']) for result in vote_result if result['value'] == 'Best')
        recommended = next(int(result['numvotes']) for result in vote_result if result['value'] == 'Recommended')
        not_recommended = next(int(result['numvotes']) for result in vote_result if result['value'] == 'Not Recommended')

        if best == 0 and recommended == 0 and not_recommended == 0:
            return "Unknown"
        if best >= recommended and best >= not_recommended:
            return "Best"
        if recommended >= best and recommended >= not_recommended:
            return "Recommended"
        return "Not recommended"

    except StopIteration as e:
        return "Unknown"


class Spreadsheet:
    def __init__(self, credentials):
        self.gc = gspread.service_account_from_dict(credentials)
        self.sh = self.gc.open_by_key('1hUAk0UGZZWCXFHJPdjmILHNI8UnDdOCfdwKneyi0Pmo')

    def create_tab(self, name, players, games):
        # delete tab if exists
        try:
            worksheet = self.sh.worksheet(name)
            self.sh.del_worksheet(worksheet)
        except WorksheetNotFound as e:
            pass

        # create new tab
        number_of_columns = 8
        games_number = len(games)
        worksheet = self.sh.add_worksheet(title=name, rows=str(games_number + 1), cols=str(number_of_columns))

        # create header
        cell_from = rowcol_to_a1(1, 1)
        cell_to = rowcol_to_a1(1, number_of_columns)
        worksheet.update(cell_from + ":" + cell_to, [
            ["Name", "Year", "Length (min.)", "Avg. weight", "Geek rating", "Avg. rating", "Users rated", "Vote"]])

        # fill with data
        cell_from = rowcol_to_a1(2, 1)
        cell_to = rowcol_to_a1(2 + games_number - 1, number_of_columns)
        games_iterator = list(
            [game["name"], game["yearpublished"], game["playingtime"], game["averageweight"], game["bayesaverage"], game["average"],
             game["usersrated"], check_fit(game, players)] for game in games)
        worksheet.update(cell_from + ":" + cell_to, games_iterator)

        # enable in tab
        worksheet.set_basic_filter()
        worksheet.columns_auto_resize(0, 1)

        # additional formatting
        # default_format = get_default_format(self.sh)
        best = CellFormat(backgroundColor=Color.fromHex('#34A853'), textFormat=TextFormat(bold=True))
        recommended = CellFormat(backgroundColor=Color.fromHex('#FBBC04'), textFormat=TextFormat(bold=True))
        not_recommended = CellFormat(backgroundColor=Color.fromHex('#EA4335'), textFormat=TextFormat(bold=True))
        unknown = CellFormat(textFormat=TextFormat(bold=True))

        number = CellFormat(numberFormat=NumberFormat(type='NUMBER', pattern='##0.00'))

        with batch_updater(self.sh) as batch:
            # some columns look better wider (header is wide)
            batch.set_column_widths(worksheet, [('B:', 50), ('C:', 110), ('D:', 100), ('E:', 100), ('F:', 100), ('G:', 100), ('H:', 130)])

            # floating numbers rounded to 2 places after coma
            batch.format_cell_range(worksheet, 'D:', number)
            batch.format_cell_range(worksheet, 'E:', number)
            batch.format_cell_range(worksheet, 'F:', number)

            # coloring by players number votes
            for i, game in enumerate(games):
                cell_from = rowcol_to_a1(2 + i, 1)
                cell_to = rowcol_to_a1(2 + i, number_of_columns)

                fit = check_fit(game, players)
                if fit == "Best":
                    batch.format_cell_range(worksheet, cell_from + ":" + cell_to, best)
                elif fit == "Recommended":
                    batch.format_cell_range(worksheet, cell_from + ":" + cell_to, recommended)
                elif fit == "Not recommended":
                    batch.format_cell_range(worksheet, cell_from + ":" + cell_to, not_recommended)
                else:
                    batch.format_cell_range(worksheet, cell_from + ":" + cell_to, unknown)