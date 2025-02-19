#!/usr/bin/env python

from flask import Flask, request, jsonify, render_template
import pandas as pd

app = Flask(__name__)

# 加载数据
df = pd.read_excel('data/Final_scores_all.xlsx')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/query', methods=['GET'])
def query():
    def get_comment(score):
        if score >= 100:
            return "Excellent work! You have achieved the highest score, demonstrating perfect mastery of the material."
        elif score >= 90:
            return "Outstanding performance! "
        elif score >= 80:
            return "Good effort! You have shown solid understanding and made progress, with room for improvement."
        elif score >= 70:
            return "Satisfactory work. You have demonstrated basic understanding, but more practice is needed."
        elif score >= 60:
            return "Needs improvement. Your performance is below average, and additional support is recommended."
        else:
            return "You can do better."

    name = request.args.get('name')
    if not name:
        return jsonify({'error': '请输入姓名！'})

    # 查找姓名
    match = df[df['name'] == name]
    if not match.empty:
        score = match['score'].values[0]
        comment = get_comment(score)
        return jsonify({
            'score': score,
            'comment': comment
        })
    else:
        return jsonify({'error': '未找到该姓名！'})

if __name__ == '__main__':
    app.run(debug=True)