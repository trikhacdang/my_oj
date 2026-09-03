import os
import sys
import random
import subprocess
import tempfile
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Giới hạn thời gian chạy cho mỗi ngôn ngữ (giây)
TIME_LIMITS = {
    "cpp": 1.0,
    "python": 3.0
}

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

# ==================== 1. TEST GENERATORS ====================
def generate_tests_quyhoach(count=100):
    tests = []
    # Test mẫu trong đề bài
    tests.append({"input": "7\n4 7 2 9 8 2 6\n", "output": "9 2"})
    
    # Test biên bổ sung
    tests.append({"input": "1\n500\n", "output": "500 500"})
    tests.append({"input": "5\n7 7 7 7 7\n", "output": "7 7"})
    tests.append({"input": "4\n1 1000000000 500 1\n", "output": "1000000000 1"})

    # Test ngẫu nhiên phân bổ theo Ràng buộc (40% N<=10^2, 30% N<=10^4, 30% N<=10^5)
    remaining = count - len(tests)
    for i in range(remaining):
        if i < 40:
            n = random.randint(1, 100)
        elif i < 70:
            n = random.randint(101, 10000)
        else:
            n = random.randint(10001, 100000)

        heights = [random.randint(1, 1000000000) for _ in range(n)]
        inp_str = f"{n}\n" + " ".join(map(str, heights)) + "\n"
        out_str = f"{max(heights)} {min(heights)}"
        tests.append({"input": inp_str, "output": out_str})
        
    return tests

def generate_tests_nguyento(count=100):
    tests = []
    # Test mẫu trong đề bài
    tests.append({"input": "11\n4 7 2 9 8 2 6 11 18 20 29\n", "output": "5"})
    
    # Test biên bổ sung
    tests.append({"input": "5\n1 4 6 8 10\n", "output": "0"})
    tests.append({"input": "4\n2 3 5 7\n", "output": "4"})

    # Test ngẫu nhiên phân bổ theo Ràng buộc (50% N<=10^2, 50% N<=10000)
    remaining = count - len(tests)
    for i in range(remaining):
        if i < 50:
            n = random.randint(1, 100)
        else:
            n = random.randint(101, 10000)

        heights = [random.randint(1, 10000) for _ in range(n)]
        prime_count = sum(1 for h in heights if is_prime(h))
        
        inp_str = f"{n}\n" + " ".join(map(str, heights)) + "\n"
        out_str = str(prime_count)
        tests.append({"input": inp_str, "output": out_str})
        
    return tests

def generate_tests_vitri(count=100):
    tests = []
    # Test mẫu trong đề bài
    tests.append({"input": "11 2\n4 7 2 9 8 2 6 11 2 2 4\n", "output": "4\n2 5 8 9"})
    
    # Test biên bổ sung
    tests.append({"input": "5 10\n1 2 3 4 5\n", "output": "NO"})
    tests.append({"input": "4 5\n5 1 2 3\n", "output": "1\n0"})

    # Test ngẫu nhiên (50% N<=10^2, 50% N<=10^5)
    remaining = count - len(tests)
    for i in range(remaining):
        if i < 50:
            n = random.randint(1, 100)
        else:
            n = random.randint(101, 100000)

        x = random.randint(1, 1000000000)
        heights = [random.randint(1, 1000000000) for _ in range(n)]
        
        if i % 2 == 0 and n > 0:
            pos_insert = random.sample(range(n), min(n, random.randint(1, 5)))
            for p in pos_insert:
                heights[p] = x

        indices = [str(idx) for idx, h in enumerate(heights) if h == x]

        inp_str = f"{n} {x}\n" + " ".join(map(str, heights)) + "\n"
        if not indices:
            out_str = "NO"
        else:
            out_str = f"{len(indices)}\n" + " ".join(indices)

        tests.append({"input": inp_str, "output": out_str})
        
    return tests

def generate_tests_somax(count=100):
    tests = []
    # Test mẫu trong đề bài
    tests.append({"input": "24101980\n", "output": "98421100"})
    
    # Test biên bổ sung
    tests.append({"input": "7\n", "output": "7"})
    tests.append({"input": "1000000000000000000\n", "output": "1000000000000000000"})

    # Test ngẫu nhiên phân bổ theo Ràng buộc (30% n<=10^3, 40% n<=10^9, 30% n<=10^18)
    remaining = count - len(tests)
    for i in range(remaining):
        if i < 30:
            n = random.randint(1, 1000)
        elif i < 70:
            n = random.randint(1001, 1000000000)
        else:
            n = random.randint(1000000001, 10**18)

        sorted_digits = "".join(sorted(str(n), reverse=True))

        inp_str = f"{n}\n"
        out_str = sorted_digits
        tests.append({"input": inp_str, "output": out_str})
        
    return tests

# ==================== 2. KHAI BÁO DANH SÁCH BÀI TẬP ====================
PROBLEMS = {
    "1": {
        "title": "Bài 1: Quy hoạch",
        "input_file": "QUYHOACH.INP",
        "output_file": "QUYHOACH.OUT",
        "gen": generate_tests_quyhoach,
        "content_html": """
            <p>Trên một dãy phố có N tòa nhà. Tòa nhà đầu tiên trên con phố có số thứ tự là 0. Tòa nhà thứ i có độ cao là h[i]. Độ cao của các toàn nhà trên con phố là các số nguyên dương. Để thực hiện việc quy hoạch thành phố, nhà nước cần tìm ra tòa nhà cao nhất và tòa nhà thấp nhất.</p>
            <p><b>Yêu cầu:</b> Cho biết tòa nhà cao nhất và tòa nhà thấp nhất trên dãy phố đó.</p>
            <p><b>Dữ liệu:</b> vào từ file văn bản <code>QUYHOACH.INP</code> gồm</p>
            <ul>
                <li>Dòng đầu chứa một số nguyên dương N là số tòa nhà (0 &le; N &le; 10<sup>6</sup>).</li>
                <li>Dòng tiếp theo chứa N số nguyên dương h[i] cách nhau khoảng trắng là độ cao của tòa nhà thứ i trong dãy phố.</li>
            </ul>
            <p><b>Kết quả:</b> ghi ra file văn bản <code>QUYHOACH.OUT</code> ghi một dòng duy nhất là độ cao của toàn nhà cao nhất là tòa nhà thấp nhất (hai số cách nhau một khoảng trắng).</p>
            <table class="example-table">
                <tr><th>QUYHOACH.INP</th><th>QUYHOACH.OUT</th></tr>
                <tr><td>7<br>4 7 2 9<br>8 2 6</td><td>9 2</td></tr>
            </table>
            <p><b>Giải thích:</b> Tòa nhà cao nhất có độ cao là 9, tòa nhà thấp nhất có độ cao là 2.</p>
            <p><b>Ràng buộc:</b></p>
            <ul>
                <li>40% số điểm của bài tương ứng với các test có N &le; 10<sup>2</sup></li>
                <li>30% số điểm của bài tương ứng với các test có N &le; 10<sup>4</sup></li>
                <li>30% số điểm còn lại không có ràng buộc nào thêm.</li>
            </ul>
        """
    },
    "2": {
        "title": "Bài 2: Số nguyên tố",
        "input_file": "NGUYENTO.INP",
        "output_file": "NGUYENTO.OUT",
        "gen": generate_tests_nguyento,
        "content_html": """
            <p>Trên một dãy phố có N tòa nhà. Tòa nhà đầu tiên trên con phố có số thứ tự là 0. Tòa nhà thứ i có độ cao là h[i]. Độ cao của các toàn nhà trên con phố là các số nguyên dương. Để thực hiện việc quy hoạch thành phố, nhà nước cần tìm ra các tòa nhà có độ cao là số nguyên tố.</p>
            <p><b>Yêu cầu:</b> Đếm số lượng tòa nhà có độ cao là số nguyên tố.</p>
            <p><b>Dữ liệu:</b> vào từ file văn bản <code>NGUYENTO.INP</code> gồm</p>
            <ul>
                <li>Dòng đầu chứa một số nguyên dương N là số tòa nhà (1 &le; N &le; 10000).</li>
                <li>Dòng tiếp theo chứa N số nguyên dương h[i] cách nhau khoảng trắng là độ cao của tòa nhà thứ i trong dãy phố (1 &le; h[i] &le; 10000).</li>
            </ul>
            <p><b>Kết quả:</b> ghi ra file văn bản <code>NGUYENTO.OUT</code> ghi một dòng duy nhất là số lượng tòa nhà có độ cao là số nguyên tố.</p>
            <table class="example-table">
                <tr><th>NGUYENTO.INP</th><th>NGUYENTO.OUT</th></tr>
                <tr><td>11<br>4 7 2 9<br>8 2 6 11 18 20 29</td><td>5</td></tr>
            </table>
            <p><b>Giải thích:</b> Có 5 toà nhà có độ cao là số nguyên tố.</p>
            <p><b>Ràng buộc:</b></p>
            <ul>
                <li>50% số điểm của bài tương ứng với các test có N &le; 10<sup>2</sup></li>
                <li>50% số điểm còn lại không có ràng buộc nào thêm.</li>
            </ul>
        """
    },
    "3": {
        "title": "Bài 3: Vị trí tòa nhà",
        "input_file": "VITRI.INP",
        "output_file": "VITRI.OUT",
        "gen": generate_tests_vitri,
        "content_html": """
            <p>Trên một dãy phố có N tòa nhà. Tòa nhà đầu tiên trên con phố có số thứ tự là 0. Tòa nhà thứ i có độ cao là h[i]. Độ cao của các toàn nhà trên con phố là các số nguyên dương. Để thực hiện việc quy hoạch thành phố, nhà nước đặt ra tiêu chuẩn sau: nếu tòa nhà nào có độ cao đúng bằng x thì tòa nhà đó đạt chuẩn quốc gia.</p>
            <p><b>Yêu cầu:</b> Đếm số lượng tòa nhà đạt chuẩn quốc gia và tìm vị trí các tòa nhà đó.</p>
            <p><b>Dữ liệu:</b> vào từ file văn bản <code>VITRI.INP</code> gồm</p>
            <ul>
                <li>Dòng đầu chứa 2 số nguyên dương N là số tòa nhà và x là độ cao chuẩn (1 &le; N &le; 10<sup>5</sup>, 1 &le; x &le; 10<sup>9</sup>).</li>
                <li>Dòng tiếp theo chứa N số nguyên dương h[i] cách nhau khoảng trắng là độ cao của tòa nhà thứ i trong dãy phố (1 &le; h[i] &le; 10<sup>9</sup>).</li>
            </ul>
            <p><b>Kết quả:</b> ghi ra file văn bản <code>VITRI.OUT</code> gồm</p>
            <ul>
                <li>Dòng đầu nếu không tìm thấy tòa nhà đặt chuẩn trong mảng thì ghi "NO", ngược lại ghi số lượng tòa nhà đạt chuẩn tìm thấy.</li>
                <li>Dòng tiếp theo ghi các vị trí của tòa nhà đặt chuẩn cách nhau khoảng trắng theo thứ tự.</li>
            </ul>
            <table class="example-table">
                <tr><th>VITRI.INP</th><th>VITRI.OUT</th></tr>
                <tr><td>11 2<br>4 7 2 9<br>8 2 6 11 2 2 4</td><td>4<br>2 5 8 9</td></tr>
            </table>
            <p><b>Giải thích:</b> Có 4 toà nhà có độ cao là 2, ở vị trí 2, 5, 8, 9.</p>
            <p><b>Ràng buộc:</b></p>
            <ul>
                <li>50% số điểm của bài tương ứng với các test có N &le; 10<sup>2</sup></li>
                <li>50% số điểm còn lại không có ràng buộc nào thêm.</li>
            </ul>
        """
    },
    "4": {
        "title": "Bài 4: Số lớn nhất",
        "input_file": "SOMAX.INP",
        "output_file": "SOMAX.OUT",
        "gen": generate_tests_somax,
        "content_html": """
            <p>Kiểu dữ liệu long long trong C++ có thể lưu trữ một số nguyên tối đa có 18 chữ số. Cho nhập vào một số nguyên dương N.</p>
            <p><b>Yêu cầu:</b> Từ các chữ số trong số nguyên dương N đã cho, hãy tạo ra số nguyên dương M có giá trị lớn nhất.</p>
            <p><b>Dữ liệu:</b> vào từ file văn bản <code>SOMAX.INP</code> cho số nguyên dương N (0 < N &le; 10<sup>18</sup>)</p>
            <p><b>Kết quả:</b> ghi ra file văn bản <code>SOMAX.OUT</code> ghi số nguyên dương M thõa yêu cầu đề bài.</p>
            <table class="example-table">
                <tr><th>SOMAX.INP</th><th>SOMAX.OUT</th></tr>
                <tr><td>24101980</td><td>98421100</td></tr>
            </table>
            <p><b>Giải thích:</b> Số lớn nhất được tạo ra từ số 24101980 là số 98421100</p>
            <p><b>Ràng buộc:</b></p>
            <ul>
                <li>30% số điểm của bài tương ứng với các test có n &le; 10<sup>3</sup></li>
                <li>40% số điểm của bài tương ứng với các test có n &le; 10<sup>9</sup></li>
                <li>30% số điểm còn lại không có ràng buộc nào thêm.</li>
            </ul>
        """
    }
}

# ==================== 3. HÀM CHẤM BÀI TỰ ĐỘNG ====================
def judge_submission(problem_id, language, code):
    prob = PROBLEMS.get(problem_id)
    if not prob:
        return "CE", "Bài tập không tồn tại."

    inp_name = prob["input_file"]
    out_name = prob["output_file"]
    tests = prob["gen"](100)

    with tempfile.TemporaryDirectory() as temp_dir:
        # Lưu file source code
        if language == "cpp":
            source_file = os.path.join(temp_dir, "solution.cpp")
            exe_file = os.path.join(temp_dir, "solution.exe")
            with open(source_file, "w", encoding="utf-8") as f:
                f.write(code)

            # Biên dịch C++
            compile_cmd = ["g++", "-O2", source_file, "-o", exe_file]
            comp_proc = subprocess.run(compile_cmd, capture_output=True, text=True)
            if comp_proc.returncode != 0:
                return "CE", f"Lỗi biên dịch (Compile Error):\n{comp_proc.stderr}"
            
            run_cmd = [exe_file]
        elif language == "python":
            source_file = os.path.join(temp_dir, "solution.py")
            with open(source_file, "w", encoding="utf-8") as f:
                f.write(code)
            
            run_cmd = [sys.executable, source_file]
        else:
            return "CE", "Ngôn ngữ không hợp lệ."

        timeout_sec = TIME_LIMITS.get(language, 2.0)

        # Tiến hành chấm 100 test cases
        for idx, test in enumerate(tests, 1):
            inp_path = os.path.join(temp_dir, inp_name)
            out_path = os.path.join(temp_dir, out_name)
            
            if os.path.exists(out_path):
                os.remove(out_path)

            with open(inp_path, "w", encoding="utf-8") as f:
                f.write(test["input"])

            try:
                proc = subprocess.run(
                    run_cmd,
                    cwd=temp_dir,
                    timeout=timeout_sec,
                    capture_output=True,
                    text=True
                )
            except subprocess.TimeoutExpired:
                return "TLE", f"Tràn thời gian (Time Limit Exceeded) tại Test {idx}/{len(tests)}"
            except Exception as e:
                return "RTE", f"Lỗi thực thi (Runtime Error) tại Test {idx}/{len(tests)}: {str(e)}"

            if proc.returncode != 0:
                return "RTE", f"Lỗi chương trình (Runtime Error) tại Test {idx}/{len(tests)}:\n{proc.stderr}"

            if not os.path.exists(out_path):
                return "WA", f"Chưa ghi kết quả ra file (Wrong Answer) tại Test {idx}/{len(tests)}: Không tìm thấy file {out_name}."

            with open(out_path, "r", encoding="utf-8") as f:
                user_output = f.read()

            # So sánh đáp án
            expected_tokens = test["output"].strip().split()
            actual_tokens = user_output.strip().split()

            if expected_tokens != actual_tokens:
                return "WA", f"Sai kết quả (Wrong Answer) tại Test {idx}/{len(tests)}."

    return "AC", f"Hoàn thành! Bạn đã vượt qua tất cả {len(tests)}/{len(tests)} test cases."

# ==================== 4. CÁC ROUTE CỦA WEB FLASK ====================
@app.route("/")
def index():
    problems_data = {}
    for pid, p in PROBLEMS.items():
        problems_data[pid] = {
            "title": p["title"],
            "input_file": p["input_file"],
            "output_file": p["output_file"],
            "content_html": p["content_html"]
        }
    return render_template("index.html", problems=problems_data)

@app.route("/submit", methods=["POST"])
def submit():
    data = request.get_json()
    problem_id = str(data.get("problem_id", "1"))
    language = data.get("language", "cpp")
    code = data.get("code", "")

    status, detail = judge_submission(problem_id, language, code)
    return jsonify({"status": status, "detail": detail})

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5000)
