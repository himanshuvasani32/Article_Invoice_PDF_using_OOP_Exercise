import pandas
from fpdf import FPDF

df = pandas.read_csv("articles.csv", dtype={"id": str})


class Article:
    def __init__(self, id):
        self.id = id
        self.name = df.loc[df["id"] == self.id, "name"].squeeze().title()
        self.price = df.loc[df["id"] == self.id, "price"].squeeze()

    def available(self):
        stock = df.loc[df["id"] == self.id, "in stock"].squeeze()
        return stock


    def buy(self):
        """This function will reduce the 1 qty from the respective article stock"""
        df.loc[df["id"] == self.id, "in stock"] = df.loc[df["id"] == self.id, "in stock"].squeeze() - 1
        df.to_csv("articles.csv", index=False)


class Receipt:

    def __init__(self, article):
        self.article = article

    def generate(self):
        pdf = FPDF(orientation="P", unit="mm", format="A4")
        pdf.add_page()

        pdf.set_font(family="Times", style="B", size=14)
        pdf.cell(w=50, h=8, txt=f"Receipt Number: {self.article.id}", ln=1, align="L")

        pdf.set_font(family="Times", style="B", size=14)
        pdf.cell(w=50, h=8, txt=f"Article: {self.article.name}", ln=1, align="L")

        pdf.set_font(family="Times", style="B", size=14)
        pdf.cell(w=50, h=8, txt=f"Price: {self.article.price}", ln=1, align="L")

        pdf.output("receipt.pdf")


print(df)

id_article = input("Enter article id to buy: ")
article = Article(id=id_article)

if article.available():
    article.buy()
    receipt = Receipt(article)
    receipt.generate()
else:
    print("Such article is not in stock.")


