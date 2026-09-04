import os
import sys
import random
import subprocess
import tempfile
from collections import Counter
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

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

# ==================== TEST GENERATORS (BÀI 1 - 12) ====================
def generate_tests_quyhoach(count=100):
    tests = []
    tests.append({"input": "7\n4 7 2 9 8 2 6\n", "output": "9 2"})
    tests.append({"input": "1\n500\n", "output": "500 500"})
    tests.append({"input": "5\n7 7 7 7 7\n", "output": "7 7"})
    tests.append({"input": "4\n1 1000000000 500 1\n", "output": "1000000000 1"})

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
    tests.append({"input": "11\n4 7 2 9 8 2 6 11 18 20 29\n", "output": "5"})
    tests.append({"input": "5\n1 4 6 8 10\n", "output": "0"})
    tests.append({"input": "4\n2 3 5 7\n", "output": "4"})

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
    tests.append({"input": "11 2\n4 7 2 9 8 2 6 11 2 2 4\n", "output": "4\n2 5 8 9"})
    tests.append({"input": "5 10\n1 2 3 4 5\n", "output": "NO"})
    tests.append({"input": "4 5\n5 1 2 3\n", "output": "1\n0"})

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
    tests.append({"input": "24101980\n", "output": "98421100"})
    tests.append({"input": "7\n", "output": "7"})
    tests.append({"input": "1000000000000000000\n", "output": "1000000000000000000"})

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

def generate_tests_xlds(count=100):
    sample_inp = "10\nLe Lo Lam\nTran Trui Trui\nNguyen Van TeO\nKaka\nCR 9\nTruong THCS Hong Bang Q5 Tp HCM\nA\nTran Thi Be cHi\nHoang Le Thong nhat chi\nTran Lam\n"
    sample_out = "2 ho ten co 1 tu\n2 ho ten co 2 tu\n3 ho ten co 3 tu\n1 ho ten co 4 tu\n1 ho ten co 5 tu\n1 ho ten co 7 tu\nTrui\nCR 9\nA\nHOANG LE THONG NHAT CHI\nTRAN THI BE CHI\nTRUONG THCS HONG BANG Q5 TP HCM\nKAKA\nLE LO LAM\nTRAN LAM\nNGUYEN VAN TEO\nTRAN TRUI TRUI"
    tests = [{"input": sample_inp, "output": sample_out}]
    
    first_names = ["An", "Binh", "Chi", "Dung", "Em", "Giang", "Hoa", "Khoa", "Lam", "Minh", "Nam", "Oanh", "Phuc", "Quan", "Son", "Tu", "Uyen", "Vinh", "Xuan", "Yen", "Trui", "Kaka", "CR 9"]
    middle_names = ["Van", "Thi", "Le", "Hoang", "THCS", "Hong Bang", "Q5", "Tp HCM", "Thong nhat", "Be"]
    
    remaining = count - len(tests)
    for i in range(remaining):
        n = random.randint(1, 100) if i < 50 else random.randint(101, 1000)
        raw_names = []
        word_counts = {}
        parsed_list = []
        
        for _ in range(n):
            num_words = random.randint(1, 7)
            words = [random.choice(first_names + middle_names) for _ in range(num_words)]
            raw_str = " ".join(words)
            raw_names.append(raw_str)
            
            word_counts[num_words] = word_counts.get(num_words, 0) + 1
            
            w_split = raw_str.strip().split()
            ten = w_split[-1]
            ho = " ".join(w_split[:-1]) if len(w_split) > 1 else ten
            parsed_list.append((ten, ho, raw_str.upper()))
            
        longest_ten = ""
        for ten, ho, upper_full in parsed_list:
            if len(ten) > len(longest_ten):
                longest_ten = ten
                
        parsed_list.sort(key=lambda x: (x[0], x[1]))
        
        res_lines = []
        for k in sorted(word_counts.keys()):
            res_lines.append(f"{word_counts[k]} ho ten co {k} tu")
        res_lines.append(longest_ten)
        for item in parsed_list:
            res_lines.append(item[2])
            
        inp_str = f"{n}\n" + "\n".join(raw_names) + "\n"
        out_str = "\n".join(res_lines)
        tests.append({"input": inp_str, "output": out_str})
    return tests

def generate_tests_giaima(count=100):
    tests = [{"input": "S1F2Y2M1E3J4G2A4K3\n", "output": "THANHNIEN"}]
    remaining = count - len(tests)
    for i in range(remaining):
        length = random.randint(1, 50) if i < 50 else random.randint(100, 500)
        inp_chars = []
        out_chars = []
        for _ in range(length):
            c = chr(random.randint(65, 90))
            d = random.randint(0, 9)
            inp_chars.append(f"{c}{d}")
            out_chars.append(chr((ord(c) - 65 + d) % 26 + 65))
        tests.append({"input": "".join(inp_chars) + "\n", "output": "".join(out_chars)})
    return tests

def generate_tests_demdoancon(count=100):
    tests = [{"input": "TATIAN\n", "output": "3"}]
    remaining = count - len(tests)
    for i in range(remaining):
        length = random.randint(5, 50) if i < 50 else random.randint(100, 1000)
        letters = [chr(random.randint(65, 90)) for _ in range(length)]
        s = "".join(letters)
        
        n = len(s)
        ans = 0
        for start in range(n):
            for end in range(start + 1, n + 1):
                sub = s[start:end]
                i_t = sub.find('T')
                if i_t != -1:
                    i_i = sub.find('I', i_t + 1)
                    if i_i != -1:
                        i_n = sub.find('N', i_i + 1)
                        if i_n != -1:
                            ans += 1
        tests.append({"input": s + "\n", "output": str(ans)})
    return tests

def generate_tests_timso(count=100):
    tests = [
        {"input": "245\n", "output": "236"},
        {"input": "9\n", "output": "0"}
    ]
    remaining = count - len(tests)
    for i in range(remaining):
        n = random.randint(1, 10000) if i < 40 else random.randint(10001, 10**12)
        s_n = str(n)
        sum_n = sum(int(c) for c in s_n)
        len_n = len(s_n)
        
        found = 0
        for cand in range(n - 1, -1, -1):
            s_c = str(cand)
            if len(s_c) == len_n and sum(int(c) for c in s_c) == sum_n:
                found = cand
                break
        tests.append({"input": f"{n}\n", "output": str(found)})
    return tests

def generate_tests_phanthuong(count=100):
    tests = [{"input": "5\n1 3 4 3 5\n3\n5 2 4\n", "output": "5 3 4"}]
    remaining = count - len(tests)
    for i in range(remaining):
        n = random.randint(1, 50) if i < 50 else random.randint(51, 1000)
        m = random.randint(1, 50) if i < 50 else random.randint(51, 1000)
        a = [random.randint(1, 100000) for _ in range(n)]
        k_list = [random.randint(1, n) for _ in range(m)]
        
        pref_max = [0] * n
        curr = 0
        for idx, val in enumerate(a):
            curr = max(curr, val)
            pref_max[idx] = curr
            
        res = [str(pref_max[k - 1]) for k in k_list]
        inp_str = f"{n}\n" + " ".join(map(str, a)) + f"\n{m}\n" + " ".join(map(str, k_list)) + "\n"
        out_str = " ".join(res)
        tests.append({"input": inp_str, "output": out_str})
    return tests

def generate_tests_lego(count=100):
    sample_inp = "4 4\n1 2 0 1\n0 0 3 0\n1 1 0 1\n2 0 2 3\n"
    tests = [{"input": sample_inp, "output": "66"}]
    remaining = count - len(tests)
    for i in range(remaining):
        m = random.randint(1, 10) if i < 50 else random.randint(11, 50)
        n = random.randint(1, 10) if i < 50 else random.randint(11, 50)
        grid = [[random.randint(0, 10) for _ in range(n)] for _ in range(m)]
        
        ans = 0
        for r in range(m):
            for c in range(n):
                h = grid[r][c]
                if h > 0:
                    ans += 1
                    top = grid[r-1][c] if r > 0 else 0
                    ans += max(0, h - top)
                    bottom = grid[r+1][c] if r < m - 1 else 0
                    ans += max(0, h - bottom)
                    left = grid[r][c-1] if c > 0 else 0
                    ans += max(0, h - left)
                    right = grid[r][c+1] if c < n - 1 else 0
                    ans += max(0, h - right)
                    
        inp_lines = [f"{m} {n}"]
        for row in grid:
            inp_lines.append(" ".join(map(str, row)))
        inp_str = "\n".join(inp_lines) + "\n"
        tests.append({"input": inp_str, "output": str(ans)})
    return tests

def generate_tests_dacbiet(count=100):
    tests = []
    tests.append({"input": "7\n2 3 7 6 8 8 6\n", "output": "3\n2"})
    tests.append({"input": "4\n5 5 5 5\n", "output": "NO"})

    remaining = count - len(tests)
    for i in range(remaining):
        n = random.randint(1, 100) if i < 50 else random.randint(101, 100000)
        heights = [random.randint(1, 1000000) for _ in range(n)]
        
        counts = Counter(heights)
        specials = [h for h, cnt in counts.items() if cnt == 1]
        
        inp_str = f"{n}\n" + " ".join(map(str, heights)) + "\n"
        if not specials:
            out_str = "NO"
        else:
            out_str = f"{len(specials)}\n{min(specials)}"
            
        tests.append({"input": inp_str, "output": out_str})
    return tests

def generate_tests_gopmang(count=100):
    sample_inp = "5\n1 2 3 4 5\n5\n6 7 8 9 10\n"
    sample_out = "6 7 8 9 10 1 2 3 4 5\n1 6 2 7 3 8 4 9 5 10"
    tests = [{"input": sample_inp, "output": sample_out}]

    remaining = count - len(tests)
    for i in range(remaining):
        n = random.randint(1, 50) if i < 50 else random.randint(51, 10000)
        m = random.randint(1, 50) if i < 50 else random.randint(51, 10000)
        a = [random.randint(1, 1000000000) for _ in range(n)]
        b = [random.randint(1, 1000000000) for _ in range(m)]

        c1 = b + a
        c2 = []
        min_len = min(n, m)
        for idx in range(min_len):
            c2.append(a[idx])
            c2.append(b[idx])
        if n > min_len:
            c2.extend(a[min_len:])
        elif m > min_len:
            c2.extend(b[min_len:])

        inp_str = f"{n}\n" + " ".join(map(str, a)) + f"\n{m}\n" + " ".join(map(str, b)) + "\n"
        out_str = " ".join(map(str, c1)) + "\n" + " ".join(map(str, c2))
        tests.append({"input": inp_str, "output": out_str})
    return tests

# ==================== TEST GENERATORS (BÀI 13 - 16 MỚI) ====================
def generate_tests_demso(count=100):
    tests = [{"input": "12 3\n2 3 3 3 5 8 8 8 7 6 7 6\n", "output": "3 8"}]
    remaining = count - len(tests)
    for i in range(remaining):
        n = random.randint(1, 1000) if i < 50 else random.randint(1001, 100000)
        k = random.randint(1, n)
        arr = [random.randint(1, 1000000) for _ in range(n)]
        
        freq = Counter(arr)
        res = []
        seen = set()
        for x in arr:
            if freq[x] >= k and x not in seen:
                res.append(str(x))
                seen.add(x)
                
        inp_str = f"{n} {k}\n" + " ".join(map(str, arr)) + "\n"
        out_str = " ".join(res) if res else "-1"
        tests.append({"input": inp_str, "output": out_str})
    return tests

def generate_tests_boiso(count=100):
    tests = [
        {"input": "12\n", "output": "12"},
        {"input": "25\n", "output": "24"}
    ]
    
    def is_beautiful(num):
        s_sum = sum(int(c) for c in str(num))
        return s_sum > 0 and num % s_sum == 0

    remaining = count - len(tests)
    for i in range(remaining):
        n = random.randint(1, 32000)
        ans = n
        while ans > 0:
            if is_beautiful(ans):
                break
            ans -= 1
        tests.append({"input": f"{n}\n", "output": str(ans)})
    return tests

def generate_tests_choncap(count=100):
    tests = [{"input": "XYXY\n", "output": "4"}]
    remaining = count - len(tests)
    
    def solve_choncap(s):
        prefix_cnt = {0: 1}
        curr = 0
        ans = 0
        for ch in s:
            curr += 1 if ch == 'X' else -1
            ans += prefix_cnt.get(curr, 0)
            prefix_cnt[curr] = prefix_cnt.get(curr, 0) + 1
        return ans

    for i in range(remaining):
        if i < 40: # 40% test: s <= 100
            length = random.randint(1, 100)
        elif i < 70: # 30% test: s <= 5000
            length = random.randint(101, 5000)
        else: # 30% test: s <= 1000000
            length = random.randint(5001, 200000)
            
        s = "".join(random.choice(['X', 'Y']) for _ in range(length))
        ans = solve_choncap(s)
        tests.append({"input": s + "\n", "output": str(ans)})
    return tests

def generate_tests_dayso(count=100):
    tests = [{"input": "5\n4 3 6 3 5\n", "output": "2"}]
    remaining = count - len(tests)
    for i in range(remaining):
        if i < 20: # 20%: n <= 50
            n = random.randint(4, 50)
            max_val = 10**9
        elif i < 40: # 20%: n <= 500
            n = random.randint(51, 500)
            max_val = 10**9
        elif i < 60: # 20%: n <= 5000
            n = random.randint(501, 5000)
            max_val = 10**9
        elif i < 80: # 20%: n <= 10^5, a[i] <= 10^5
            n = random.randint(5001, 10000)
            max_val = 100000
        else: # 20% còn lại
            n = random.randint(5001, 10000)
            max_val = 10**9

        a = [random.randint(1, max_val) for _ in range(n)]
        
        # Chuẩn bị giải đáp án mẫu cho test ngẫu nhiên
        sums_freq = {}
        for x in range(n):
            for y in range(x + 1, n):
                s = a[x] + a[y]
                sums_freq[s] = sums_freq.get(s, 0) + 1

        ans = 0
        for p in range(n):
            target = 3 * a[p]
            valid = False
            for j in range(n):
                if j == p:
                    continue
                rem = target - a[j]
                
                # Loại trừ các cặp chứa index j hoặc p
                invalid_cnt = 0
                for other in [p, j]:
                    s_check = a[j] + a[other]
                    if s_check == rem:
                        invalid_cnt += 1
                
                total_c = sums_freq.get(rem, 0)
                if total_c - invalid_cnt > 0:
                    valid = True
                    break
            if valid:
                ans += 1

        inp_str = f"{n}\n" + " ".join(map(str, a)) + "\n"
        tests.append({"input": inp_str, "output": str(ans)})
    return tests

# ==================== DANH SÁCH BÀI TẬP (16 BÀI) ====================
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
                <tr><td>7<br>4 7 2 9 8 2 6</td><td>9 2</td></tr>
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
                <tr><td>11<br>4 7 2 9 8 2 6 11 18 20 29</td><td>5</td></tr>
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
                <tr><td>11 2<br>4 7 2 9 8 2 6 11 2 2 4</td><td>4<br>2 5 8 9</td></tr>
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
    },
    "5": {
        "title": "Bài 5: Xử lý danh sách",
        "input_file": "XLDS.INP",
        "output_file": "XLDS.OUT",
        "gen": generate_tests_xlds,
        "content_html": """
            <p>Cho một danh sách họ tên của N người, tên là từ cuối cùng ở bên phải trong chuỗi họ tên, các từ còn lại là họ. Trường hợp họ tên có 1 từ thì từ đó vừa là tên và vừa là họ. Các từ cách nhau một khoảng trắng và không có khoảng trắng ở đầu.</p>
            <p><b>Yêu cầu:</b></p>
            <ul>
                <li>Đếm xem có bao nhiêu họ tên có 1, 2, 3, … i từ?</li>
                <li>Tìm tên dài nhất, nếu có nhiều tên dài như nhau thì lấy tên dài nhất đầu tiên trong danh sách. Đổi tất cả họ tên trong danh sách thành chữ in hoa.</li>
                <li>Sắp xếp lại danh sách ban đầu tăng dần theo bảng mã ASCII với ưu tiên 1 là tên và ưu tiên 2 là họ.</li>
            </ul>
            <p><b>Dữ liệu:</b> vào từ file văn bản <code>XLDS.INP</code> gồm</p>
            <ul>
                <li>Dòng đầu chứa số nguyên dương N (0 < N &le; 10000)</li>
                <li>N dòng tiếp theo, mỗi dòng ghi một họ tên của một người.</li>
            </ul>
            <p><b>Kết quả:</b> ghi ra file văn bản <code>XLDS.OUT</code> ghi như định dạng của ví dụ</p>
            <ul>
                <li>Liệt kê có bao nhiêu họ tên có 1, 2, 3, …, i từ</li>
                <li>Dòng tiếp theo ghi ra tên dài nhất trong danh sách.</li>
                <li>N dòng tiếp theo ghi ra danh sách họ tên đã được đổi sang chữ in hoa và đã được sắp xếp tăng dần theo thứ tự ưu tiên 1 là tên và ưu tiên 2 là họ</li>
            </ul>
            <table class="example-table">
                <tr><th>XLDS.INP</th><th>XLDS.OUT</th></tr>
                <tr>
                    <td>10<br>Le Lo Lam<br>Tran Trui Trui<br>Nguyen Van TeO<br>Kaka<br>CR 9<br>Truong THCS Hong Bang Q5 Tp HCM<br>A<br>Tran Thi Be cHi<br>Hoang Le Thong nhat chi<br>Tran Lam</td>
                    <td>2 ho ten co 1 tu<br>2 ho ten co 2 tu<br>3 ho ten co 3 tu<br>1 ho ten co 4 tu<br>1 ho ten co 5 tu<br>1 ho ten co 7 tu<br>Trui<br>CR 9<br>A<br>HOANG LE THONG NHAT CHI<br>TRAN THI BE CHI<br>TRUONG THCS HONG BANG Q5 TP HCM<br>KAKA<br>LE LO LAM<br>TRAN LAM<br>NGUYEN VAN TEO<br>TRAN TRUI TRUI</td>
                </tr>
            </table>
            <p><b>Ràng buộc:</b></p>
            <ul>
                <li>50% số điểm của bài tương ứng với các test có N &le; 100</li>
                <li>50% số điểm còn lại không có ràng buộc nào thêm.</li>
            </ul>
        """
    },
    "6": {
        "title": "Bài 6: Giải mã",
        "input_file": "GIAIMA.INP",
        "output_file": "GIAIMA.OUT",
        "gen": generate_tests_giaima,
        "content_html": """
            <p>Trong hoạt động Hội trại kỷ niệm tháng Thanh niên, Đoàn trường tổ chức trò chơi lớn đó là "Giải mã mật thư". Bạn Minh nhận được một mật thư từ ban tổ chức với nội dung là một xâu kí tự đã được mã hóa theo quy luật. Xâu kí tự này gồm các cặp chữ cái tiếng Anh viết hoa và chữ số từ 0 đến 9 liên tiếp nhau, mật thư được giải mã theo quy luật dịch chuyển vòng tròn chữ cái.</p>
            <p><b>Ví dụ:</b> Xâu kí tự trong mật thư là 'R2F3M1' được giải mã theo quy luật: Kí tự 'R' dịch chuyển thêm 2 vị trí được kí tự 'T', kí tự 'F' dịch chuyển thêm 3 vị trí được kí tự T, kí tự 'M' dịch chuyển thêm 1 vị trí được kí tự 'N'. Vậy dòng văn bản 'R2F3M1' sau khi giải mã có kết quả là “TIN'.</p>
            <p><b>Yêu cầu:</b> Hãy lập trình giúp Nam giải mã mật thư mà ban tổ chức đã cho.</p>
            <p><b>Dữ liệu:</b> vào từ file văn bản <code>GIAIMA.INP</code> gồm một chuỗi kí tự chỉ chứa từng cặp chữ cái tiếng anh viết in và chữ số từ 0 đến 9 liên tục nhau. Chuỗi có độ dài tối đa 10<sup>6</sup> kí tự.</p>
            <p><b>Kết quả:</b> ghi ra file văn bản <code>GIAIMA.OUT</code> ghi chuỗi đã được giải mã.</p>
            <table class="example-table">
                <tr><th>GIAIMA.INP</th><th>GIAIMA.OUT</th></tr>
                <tr><td>S1F2Y2M1E3J4G2A4K3</td><td>THANHNIEN</td></tr>
            </table>
            <p><b>Ràng buộc:</b></p>
            <ul>
                <li>50% số điểm của bài tương ứng với các test chứa chuỗi có độ dài nhỏ hơn 1000 kí tự</li>
                <li>50% số điểm còn lại không có ràng buộc nào thêm.</li>
            </ul>
        """
    },
    "7": {
        "title": "Bài 7: Đếm đoạn con",
        "input_file": "DEMDOANCON.INP",
        "output_file": "DEMDOANCON.OUT",
        "gen": generate_tests_demdoancon,
        "content_html": """
            <p>Chuỗi kí tự X được gọi là chuỗi con của Y khi chuỗi X được tạo thành bằng cách xóa đi một số kí tự (có thể không cần xóa kí tự nào) của Y mà không thay đổi trật tự sắp xếp vốn có của các kí tự trong Y. Ví dụ: chuỗi ABC là một chuỗi con của ADBC nhưng ACB thì không. Chuỗi kí tự A được gọi là một đoạn con của chuỗi B khi chuỗi A được tạo thành bằng cách chọn một đoạn kí tự liên tiếp nào đó của chuỗi B. Ví dụ: chuỗi XYZ là một đoạn con của chuỗi AXYZZ nhưng AYZ thì không. Cho xâu S gồm N chữ cái in hoa. Khoa muốn chọn một đoạn con của S sao cho đoạn con này có chứa chuỗi con là TIN</p>
            <p><b>Yêu cầu:</b> Đếm số đoạn con khác nhau mà Khoa có thể chọn biết rằng 2 đoạn con khác nhau khi có ít nhất một vị trí được chọn khác nhau.</p>
            <p><b>Dữ liệu:</b> vào từ file văn bản <code>DEMDOANCON.INP</code> gồm một chuỗi kí tự chứa các chữ cái tiếng Anh in hoa và không có khoảng trắng. Độ dài tối đa của chuỗi là 100000 kí tự.</p>
            <p><b>Kết quả:</b> ghi ra file văn bản <code>DEMDOANCON.OUT</code> ghi một số nguyên duy nhất là số đoạn con khác nhau mà Khoa có thể chọn được.</p>
            <table class="example-table">
                <tr><th>DEMDOANCON.INP</th><th>DEMDOANCON.OUT</th></tr>
                <tr><td>TATIAN</td><td>3</td></tr>
            </table>
            <p><b>Ràng buộc:</b></p>
            <ul>
                <li>50% số điểm của bài tương ứng với các test chứa chuỗi có độ dài &le; 100</li>
                <li>25% số điểm của bài tương ứng với các test chứa chuỗi có độ dài &le; 10000</li>
                <li>25% số điểm còn lại không có ràng buộc nào thêm.</li>
            </ul>
        """
    },
    "8": {
        "title": "Bài 8: Tìm số",
        "input_file": "TIMSO.INP",
        "output_file": "TIMSO.OUT",
        "gen": generate_tests_timso,
        "content_html": """
            <p>Cho số tự nhiên N, tìm số tự nhiên A thỏa mãn các điều kiện sau:</p>
            <ul>
                <li>A < N</li>
                <li>A lớn nhất có thể.</li>
                <li>Số lượng chữ số của A bằng số lượng chữ số của N</li>
                <li>Tổng các chữ số của A bằng tổng các chữ số của N</li>
            </ul>
            <p><b>Yêu cầu:</b> Hãy tìm số thõa điều kiện của đề bài.</p>
            <p><b>Dữ liệu:</b> vào từ file văn bản <code>TIMSO.INP</code> nhập số nguyên dương N (0 &le; N &le; 10<sup>15</sup>)</p>
            <p><b>Kết quả:</b> ghi ra file văn bản <code>TIMSO.OUT</code> ghi ra số A duy nhất thỏa điều kiện của đề bài. Nếu không tìm được số nào thỏa mãn thì ghi ra 0.</p>
            <table class="example-table">
                <tr><th>TIMSO.INP</th><th>TIMSO.OUT</th></tr>
                <tr><td>245</td><td>236</td></tr>
                <tr><td>9</td><td>0</td></tr>
            </table>
            <p><b>Ràng buộc:</b></p>
            <ul>
                <li>40% số điểm của bài tương ứng với các test có N &le; 10<sup>4</sup></li>
                <li>30% số điểm của bài tương ứng với các test có N &le; 10<sup>9</sup></li>
                <li>30% số điểm còn lại không có ràng buộc nào thêm.</li>
            </ul>
        """
    },
    "9": {
        "title": "Bài 9: Phần thưởng",
        "input_file": "PHANTHUONG.INP",
        "output_file": "PHANTHUONG.OUT",
        "gen": generate_tests_phanthuong,
        "content_html": """
            <p>Trung thu năm nay chị Hằng chuẩn bị N phần quà được đánh số từ 1 đến N, phần quà thứ i (1 &le; i &le; n) có giá trị là Ai. Có M học sinh, mỗi học sinh có 1 phiếu bé ngoan được đánh số K. Học sinh được sử dụng phiếu bé ngoan chọn một phần quà có giá trị lớn nhất trong K phần quà đầu tiên. Cho biết số lượng của một phần quà là vô hạn.</p>
            <p><b>Yêu cầu:</b> Hãy giúp chú Cuội tính giá trị phần quà lớn nhất mà mỗi học sinh được nhận.</p>
            <p><b>Dữ liệu:</b> Vào từ file văn bản <code>PHANTHUONG.INP</code></p>
            <ul>
                <li>Dòng đầu chứa nhập N (0 < n &le; 10<sup>5</sup>)</li>
                <li>Dòng 2 chứa N số nguyên dương Ai (1 &le; Ai &le; 10<sup>9</sup>)</li>
                <li>Dòng 3 chứa số nguyên dương M (0 < m &le; 10<sup>5</sup>)</li>
                <li>Dòng 4 chứa m số nguyên K (1 &le; K &le; N)</li>
            </ul>
            <p><b>Kết quả:</b> ghi ra file văn bản <code>PHANTHUONG.OUT</code> Ghi các số thõa mãn yêu cầu đề bài, mỗi số cách nhau khoảng trắng.</p>
            <table class="example-table">
                <tr><th>PHANTHUONG.INP</th><th>PHANTHUONG.OUT</th></tr>
                <tr><td>5<br>1 3 4 3 5<br>3<br>5 2 4</td><td>5 3 4</td></tr>
            </table>
            <p><b>Ràng buộc:</b></p>
            <ul>
                <li>50% số điểm của bài tương ứng với các test có N, M &le; 100</li>
                <li>25% số điểm của bài tương ứng với các test có N, M &le; 10<sup>4</sup></li>
                <li>25% số điểm còn lại không có ràng buộc nào thêm.</li>
            </ul>
        """
    },
    "10": {
        "title": "Bài 10: Sơn lego",
        "input_file": "LEGO.INP",
        "output_file": "LEGO.OUT",
        "gen": generate_tests_lego,
        "content_html": """
            <p>Hè về, Minh và Khoa chơi xây tháp bằng các khối lego màu trắng hình khối lập phương với kích thước cạnh là 1 đơn vị trên một tấm đế có kích thước M dòng và N cột. Sau khi xây xong hai bạn tiến hành sơn màu các bề mặt nhìn thấy được của tòa tháp.</p>
            <p><b>Yêu cầu:</b> Hãy giúp Minh và Khoa đếm số mặt cần sơn.</p>
            <p><b>Dữ liệu:</b> vào từ file văn bản <code>LEGO.INP</code></p>
            <ul>
                <li>Dòng đầu tiên chứa số nguyên M và N (1 &le; M, N &le; 200)</li>
                <li>M dòng tiếp theo mỗi dòng chứa N số nguyên dương cách nhau khoảng trắng biểu thị số khối lego chồng lên nhau tại vị trí đó.</li>
            </ul>
            <p><b>Kết quả:</b> ghi ra file văn bản <code>LEGO.OUT</code> ghi số mặt cần sơn.</p>
            <table class="example-table">
                <tr><th>LEGO.INP</th><th>LEGO.OUT</th></tr>
                <tr><td>4 4<br>1 2 0 1<br>0 0 3 0<br>1 1 0 1<br>2 0 2 3</td><td>66</td></tr>
            </table>
            <p><b>Ràng buộc:</b></p>
            <ul>
                <li>50% số điểm của bài tương ứng với các test có M, N &le; 50</li>
                <li>50% số điểm còn lại không có ràng buộc nào thêm.</li>
            </ul>
        """
    },
    "11": {
        "title": "Bài 11: Tòa nhà đặc biệt",
        "input_file": "DACBIET.INP",
        "output_file": "DACBIET.OUT",
        "gen": generate_tests_dacbiet,
        "content_html": """
            <p>Trên một dãy phố có N tòa nhà. Tòa nhà đầu tiên trên con phố có số thứ tự là 0. Tòa nhà thứ i có độ cao là h[i]. Độ cao của các toàn nhà trên con phố là các số nguyên dương. Để thực hiện việc quy hoạch thành phố, nhà nước đặt ra tiêu chuẩn sau: nếu độ cao của tòa nhà nào chỉ xuất hiện 1 lần trên dãy phố thì tòa nhà đó là “đặc biệt”.</p>
            <p><b>Yêu cầu:</b> Đếm số lượng tòa nhà “đặc biệt”.</p>
            <p><b>Dữ liệu:</b> vào từ file văn bản <code>DACBIET.INP</code> gồm</p>
            <ul>
                <li>Dòng đầu chứa một số nguyên dương N là số tòa nhà (1 &le; N &le; 10<sup>5</sup>).</li>
                <li>Dòng tiếp theo chứa N số nguyên dương h[i] cách nhau khoảng trắng là độ cao của tòa nhà thứ i trong dãy phố (1 &le; h[i] &le; 10<sup>6</sup>)</li>
            </ul>
            <p><b>Kết quả:</b> ghi ra file văn bản <code>DACBIET.OUT</code> gồm</p>
            <ul>
                <li>Dòng đầu nếu không có tòa nhà đặc biệt thì ghi "NO”, ngược lại ghi số lượng tòa nhà đặc biệt tìm thấy.</li>
                <li>Dòng tiếp theo ghi chiều cao nhỏ nhất của các tòa nhà đặc biệt.</li>
            </ul>
            <table class="example-table">
                <tr><th>DACBIET.INP</th><th>DACBIET.OUT</th></tr>
                <tr><td>7<br>2 3 7 6 8 8 6</td><td>3<br>2</td></tr>
            </table>
            <p><b>Giải thích:</b> Có 3 tòa nhà đặc biệt với chiều cao là 2, 3, 7 và tòa nhà đặc biệt có chiều cao nhỏ nhất là 2.</p>
            <p><b>Ràng buộc:</b></p>
            <ul>
                <li>50% số điểm của bài tương ứng với các test có n &le; 10<sup>2</sup>.</li>
                <li>50% số điểm của bài tương ứng với các test có n &le; 10<sup>5</sup>.</li>
            </ul>
        """
    },
    "12": {
        "title": "Bài 12: Gộp mảng theo yêu cầu",
        "input_file": "GOPMANG.INP",
        "output_file": "GOPMANG.OUT",
        "gen": generate_tests_gopmang,
        "content_html": """
            <p>Trong một bài toán xử lý dữ liệu, người ta thường cần kết hợp các dãy số để thuận tiện cho việc lưu trữ và xử lý.</p>
            <p>Cho hai mảng số nguyên A và B. Hai mảng được đánh số từ 1 đến số phần tử của mỗi mảng.</p>
            <p><b>Yêu cầu thực hiện hai cách gộp mảng sau:</b></p>
            <ul>
                <li><b>Cách 1:</b> Tạo mảng C bằng cách đưa toàn bộ các phần tử của mảng B vào trước, sau đó đưa toàn bộ các phần tử của mảng A vào sau.</li>
                <li><b>Cách 2:</b> Tạo mảng C bằng cách lần lượt lấy một phần tử của A, rồi một phần tử của B, cứ như vậy cho đến khi đã sử dụng hết phần tử của một trong hai mảng. Nếu một mảng còn phần tử chưa được sử dụng thì đưa các phần tử còn lại vào cuối mảng C.</li>
            </ul>
            <p>Hãy lập trình thực hiện hai cách gộp trên và in kết quả.</p>
            <p><b>Dữ liệu:</b> Vào từ file văn bản <code>GOPMANG.INP</code>:</p>
            <ul>
                <li>Dòng thứ nhất chứa số nguyên n là số phần tử của mảng A (1 &le; n &le; 10<sup>5</sup>).</li>
                <li>Dòng thứ hai chứa n số nguyên là các phần tử của mảng A (1 &le; a[i] &le; 10<sup>9</sup>).</li>
                <li>Dòng thứ ba chứa số nguyên m là số phần tử của mảng B (1 &le; m &le; 10<sup>5</sup>).</li>
                <li>Dòng thứ tư chứa m số nguyên là các phần tử của mảng B (1 &le; b[i] &le; 10<sup>9</sup>).</li>
            </ul>
            <p>Các phần tử trên cùng một dòng được phân cách bởi một khoảng trắng.</p>
            <p><b>Kết quả:</b> Ghi ra file kết quả <code>GOPMANG.OUT</code>:</p>
            <ul>
                <li>Dòng thứ nhất in các phần tử của mảng C sau khi gộp theo Cách 1.</li>
                <li>Dòng thứ hai in các phần tử của mảng C sau khi gộp theo Cách 2.</li>
            </ul>
            <p>Các phần tử trên mỗi dòng được phân cách bởi một khoảng trắng.</p>
            <table class="example-table">
                <tr><th>GOPMANG.INP</th><th>GOPMANG.OUT</th></tr>
                <tr><td>5<br>1 2 3 4 5<br>5<br>6 7 8 9 10</td><td>6 7 8 9 10 1 2 3 4 5<br>1 6 2 7 3 8 4 9 5 10</td></tr>
            </table>
            <p><b>Ràng buộc:</b></p>
            <ul>
                <li>50% số điểm có n, m &le; 10<sup>2</sup>.</li>
                <li>50% số điểm còn lại không có ràng buộc gì thêm.</li>
            </ul>
        """
    },
    "13": {
        "title": "Bài 13: Đếm số",
        "input_file": "DEMSO.INP",
        "output_file": "DEMSO.OUT",
        "gen": generate_tests_demso,
        "content_html": """
            <p>Cho một dãy A có N số nguyên dương và một số nguyên dương K.</p>
            <p><b>Yêu cầu:</b> Hãy xuất ra các phần tử có số lần xuất hiện trong dãy A từ K lần trở lên (mỗi số chỉ xuất 01 lần).</p>
            <p><b>Dữ liệu:</b> Vào từ file văn bản <code>DEMSO.INP</code>:</p>
            <ul>
                <li>Dòng thứ nhất chứa 2 số nguyên dương N, K (1 &le; n, k &le; 5 . 10<sup>5</sup>).</li>
                <li>Dòng tiếp theo chứa N số nguyên a[i] (1 &le; a[i] &le; 10<sup>6</sup>)</li>
            </ul>
            <p><b>Kết quả:</b> Ghi ra file văn bản <code>DEMSO.OUT</code> gồm một dòng là các số thỏa điều kiện trên (các số cách nhau khoảng trắng), trường hợp không có số nào thỏa thì xuất số -1.</p>
            <table class="example-table">
                <tr><th>DEMSO.INP</th><th>DEMSO.OUT</th></tr>
                <tr><td>12 3<br>2 3 3 3 5 8 8 8 7 6 7 6</td><td>3 8</td></tr>
            </table>
            <p><b>Ràng buộc:</b> 100% số điểm theo yêu cầu đề bài.</p>
        """
    },
    "14": {
        "title": "Bài 14: Tìm bội số",
        "input_file": "BOISO.INP",
        "output_file": "BOISO.OUT",
        "gen": generate_tests_boiso,
        "content_html": """
            <p>Cho một số nguyên dương n. Số n được gọi là “số đẹp trai” nếu n có là bội của tổng tất cả các chữ số của nó.</p>
            <p><b>Yêu cầu:</b> Nếu n là “số đẹp trai” thì in ra số n, nếu không thì in ra số nguyên dương m nhỏ hơn và gần n nhất thỏa mãn m là “số đẹp trai”.</p>
            <p><b>Dữ liệu:</b> Vào từ file văn bản <code>BOISO.INP</code> chứa số nguyên dương n (1 &le; n &le; 32000).</p>
            <p><b>Kết quả:</b> Ghi ra file văn bản <code>BOISO.OUT</code> gồm một số nguyên là kết quả của bài toán.</p>
            <table class="example-table">
                <tr><th>BOISO.INP</th><th>BOISO.OUT</th></tr>
                <tr><td>12</td><td>12</td></tr>
                <tr><td>25</td><td>24</td></tr>
            </table>
            <p><b>Ràng buộc:</b> 100% số điểm theo yêu cầu đề bài.</p>
        """
    },
    "15": {
        "title": "Bài 15: Chọn cặp",
        "input_file": "CHONCAP.INP",
        "output_file": "CHONCAP.OUT",
        "gen": generate_tests_choncap,
        "content_html": """
            <p>Cho một xâu kí tự s chỉ gồm 2 kí tự X và Y.</p>
            <p><b>Yêu cầu:</b> Đếm số cách chọn cặp chỉ số (i, j) mà xâu con liên tiếp từ kí tự thứ i đến kí tự thứ j của xâu S có số lượng kí tự X bằng số lượng kí tự Y.</p>
            <p><b>Dữ liệu:</b> Vào từ file văn bản <code>BOISO.INP</code> chứa xâu s (1 &le; s &le; 10<sup>6</sup>).</p>
            <p><b>Kết quả:</b> Ghi ra file văn bản <code>BOISO.OUT</code> gồm một số nguyên là kết quả của bài toán.</p>
            <table class="example-table">
                <tr><th>BOISO.INP</th><th>BOISO.OUT</th></tr>
                <tr><td>XYXY</td><td>4</td></tr>
            </table>
            <p><b>Ràng buộc:</b></p>
            <ul>
                <li>40% số điểm của bài tương ứng với các test có s &le; 100.</li>
                <li>30% số điểm của bài tương ứng với các test có s &le; 5000.</li>
                <li>30% số điểm còn lại không có ràng buộc gì thêm.</li>
            </ul>
        """
    },
    "16": {
        "title": "Bài 16: Dãy số",
        "input_file": "DAYSO.INP",
        "output_file": "DAYSO.OUT",
        "gen": generate_tests_dayso,
        "content_html": """
            <p>Cho một dãy A có N số nguyên dương. Số a[p] (1 &le; p &le; n) được gọi là một số trung bình cộng trong dãy nếu tồn tại 3 chỉ số i, j, k (1 &le; i, j, k &le; n) đôi một khác nhau, sao cho a[p] = (a[i] + a[j] + a[k]) &divide; 3.</p>
            <p><b>Yêu cầu:</b> Hãy tìm số lượng các số trung bình cộng trong dãy.</p>
            <p><b>Dữ liệu:</b> Vào từ file văn bản <code>DAYSO.INP</code>:</p>
            <ul>
                <li>Dòng thứ nhất chứa 2 số nguyên dương N (1 &le; n &le; 10<sup>5</sup>).</li>
                <li>Dòng tiếp theo chứa N số nguyên a[i] (1 &le; a[i] &le; 10<sup>9</sup>)</li>
            </ul>
            <p><b>Kết quả:</b> Ghi ra file văn bản <code>DAYSO.OUT</code> gồm một số nguyên là kết quả bài toán.</p>
            <table class="example-table">
                <tr><th>DEMSO.INP</th><th>DEMSO.OUT</th></tr>
                <tr><td>5<br>4 3 6 3 5</td><td>2</td></tr>
            </table>
            <p><b>Ràng buộc:</b></p>
            <ul>
                <li>20% số điểm của bài tương ứng với các test có n &le; 50.</li>
                <li>20% số điểm của bài tương ứng với các test có n &le; 500.</li>
                <li>20% số điểm của bài tương ứng với các test có n &le; 5000.</li>
                <li>20% số điểm của bài tương ứng với các test có n &le; 10<sup>5</sup>, a[i] &le; 10<sup>5</sup>.</li>
                <li>20% số điểm còn lại không có ràng buộc gì thêm.</li>
            </ul>
        """
    }
}

# ==================== JUDGE ENGINE ====================
def judge_submission(problem_id, language, code):
    prob = PROBLEMS.get(problem_id)
    if not prob:
        return "CE", "Bài tập không tồn tại."

    inp_name = prob["input_file"]
    out_name = prob["output_file"]
    tests = prob["gen"](100)

    with tempfile.TemporaryDirectory() as temp_dir:
        if language == "cpp":
            source_file = os.path.join(temp_dir, "solution.cpp")
            exe_file = os.path.join(temp_dir, "solution.exe")
            with open(source_file, "w", encoding="utf-8") as f:
                f.write(code)

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

            expected_tokens = test["output"].strip().split()
            actual_tokens = user_output.strip().split()

            if expected_tokens != actual_tokens:
                return "WA", f"Sai kết quả (Wrong Answer) tại Test {idx}/{len(tests)}."

    return "AC", f"Hoàn thành! Bạn đã vượt qua tất cả {len(tests)}/{len(tests)} test cases."

# ==================== FLASK ROUTES ====================
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
