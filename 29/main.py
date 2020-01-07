import view
from bill import Bill
from flask import Flask, request, session, render_template, session

app = Flask(__name__)
bill = None

def main():
    action = "Start"

    while action != "End":
        action = input("What you want to do? [Add meal, Add service, Sum, Discount, Check, Save, End]: ")

        if action == "Add meal":
            name, price = view.ask_for_meal()
            if name is None or price is None:
                continue
            bill.add_meal(name, price)
        elif action == "Add service":
            name, price, guest_number = view.ask_for_service()
            if name is None or price is None or guest_number is None:
                continue
            bill.add_service(name, price, guest_number)
        elif action == "Sum":
            print(bill.calculate())
        elif action == "Discount":
            discount = view.ask_for_discount()
            if discount is None:
                continue
            print(bill.calculate_with_discount(discount))
        elif action == "Check":
            overall_sum, discount = view.ask_for_check_discount()
            if overall_sum is None or discount is None:
                continue
            print(Bill.check_discount(overall_sum, discount))
        elif action == "Save":
            filename = view.ask_for_filename()
            bill.print_to_file(filename)


@app.route('/add_meal', methods=['POST'])
def add_meal():
    bill = Bill()
    if 'entries' in session:
        entries = session['entries']
        bill.entries = entries

    name = request.form['meal_name']
    price = float(request.form['meal_price'])
    bill.add_meal(name, price)
    session['entries'] = bill.entries
    return "Success"


@app.route('/add_meal_form')
def add_meal_form():
    render_template('add_meal_form.html')


@app.route('/sum')
def sum():
    bill = Bill()
    if 'entries' in session:
        entries = session['entries']
        bill.entries = entries
    return f"Overall sum: {bill.calculate()}"


if __name__ == '__main__':
    app.secret_key = "secret value"
    app.run(debug=True)
