from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# ================= HOME =================
@app.route('/')
def index():
    return render_template('index.html')


# ================= PRODUKSI =================
@app.route('/produksi', methods=['GET', 'POST'])
def produksi():
    result = None

    if request.method == 'POST':
        try:
            waktu_list = request.form.getlist('waktu[]')
            data = []
            for w in waktu_list:
                val = float(w.strip())
                if val > 0:
                    data.append(val)
            
            if data:
                bottleneck = max(data)
                total = sum(data)
                n = len(data)
                efisiensi = (total / (n * bottleneck)) * 100

                result = {
                    "data": [round(x, 1) for x in data],
                    "bottleneck": round(bottleneck, 1),
                    "efisiensi": round(efisiensi, 2)
                }
        except (ValueError, ZeroDivisionError):
            pass  # Silent fail, result remains None

    return render_template('produksi.html', result=result)


# ================= SHIFT =================
@app.route('/shift', methods=['GET', 'POST'])
def shift():
    jadwal = None

    if request.method == 'POST':
        nama_list = request.form.getlist('nama[]')
        # Filter non-empty names
        nama = [n.strip() for n in nama_list if n.strip()]
        
        if not nama:
            jadwal = {"Shift 1": [], "Shift 2": []}
        else:
            # Split fairly into two shifts
            mid = len(nama) // 2
            shift1 = nama[:mid]
            shift2 = nama[mid:]
            jadwal = {
                "Shift 1": shift1,
                "Shift 2": shift2
            }

    return render_template('shift.html', jadwal=jadwal)


# ================= INVENTORY =================
@app.route('/inventory', methods=['GET', 'POST'])
def inventory():
    rop = None
    status = None

    if request.method == 'POST':
        try:
            stok = float(request.form['stok'])
            demand = float(request.form['demand'])
            lead_time = float(request.form['lead_time'])

            if demand > 0 and lead_time > 0:
                rop = round(demand * lead_time)
                if stok <= rop:
                    status = "🔴 Harus Reorder"
                else:
                    status = "🟢 Aman"
        except ValueError:
            pass

    return render_template('inventory.html', rop=rop, status=status)


if __name__ == '__main__':
    app.run(debug=True)