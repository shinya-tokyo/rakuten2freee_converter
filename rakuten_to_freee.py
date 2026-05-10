#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
楽天証券の取引報告書CSVをfreeeの仕訳形式に変換
"""

import csv
import sys
from datetime import datetime

def parse_rakuten_csv(input_file):
    """楽天証券CSVを読み込む（Shift-JIS対応）"""
    with open(input_file, 'r', encoding='cp932') as f:
        content = f.read()

    lines = content.split('\n')

    # 「国内株式(現物取引)」セクションを抽出
    gensoku_start = None
    gensoku_end = None

    for i, line in enumerate(lines):
        if '国内株式(現物取引)' in line:
            gensoku_start = i
        elif gensoku_start is not None and '---' in line and gensoku_end is None:
            gensoku_end = i
            break

    if gensoku_start is None:
        print("エラー: 現物株式セクションが見つかりません")
        return []

    # ヘッダーとデータ行を抽出
    header_line = lines[gensoku_start + 1]
    data_lines = lines[gensoku_start + 2:gensoku_end]

    # CSVとしてパース
    reader = csv.DictReader(
        [header_line] + data_lines,
        skipinitialspace=True
    )

    transactions = []
    for row in reader:
        # 空行をスキップ
        if not row.get('銘柄名', '').strip():
            continue

        # 売買区分が「買付」のみを対象
        if row.get('売買区分', '').strip() != '買付':
            continue

        try:
            # 約定日をパース
            yakujo_date = row.get('約定日', '').strip()
            if not yakujo_date:
                continue

            # 約定金額をパース
            yakujo_amount = row.get('約定金額', '').strip().replace(',', '')
            if not yakujo_amount:
                continue

            amount = int(yakujo_amount)

            # 銘柄名と数量から摘要を作成
            meigara = row.get('銘柄名', '').strip()
            suryo = row.get('数量', '').strip()

            transactions.append({
                'date': yakujo_date,
                'meigara': meigara,
                'suryo': suryo,
                'amount': amount,
                'row': row
            })
        except (ValueError, KeyError) as e:
            print(f"警告: 行のパースに失敗しました: {e}")
            continue

    return transactions

def convert_to_freee_format(transactions):
    """freee仕訳形式に変換"""
    freee_rows = [
        ['日付', '借方科目', '借方金額', '貸方科目', '貸方金額', '摘要']
    ]

    for tx in transactions:
        date = tx['date']
        amount = tx['amount']
        meigara = tx['meigara'].strip()
        suryo = tx['suryo'].strip()

        # 摘要を作成
        remarks = f"{meigara} {suryo}株買付"

        freee_rows.append([
            date,
            '有価証券',
            str(amount),
            '普通預金',
            str(amount),
            remarks
        ])

    return freee_rows

def main():

    print("input_file >>")
    input_file = input()
    print("input_file is" + input_file)

    print("output_file >>")
    output_file = input()
    print("ouput_file is" + output_file)


    print(f"読み込み中: {input_file}")
    transactions = parse_rakuten_csv(input_file)

    if not transactions:
        print("変換対象の買付取引がありません")
        return

    print(f"変換対象: {len(transactions)}件の買付取引")

    # freee形式に変換
    freee_rows = convert_to_freee_format(transactions)

    # UTF-8で出力
    with open(output_file, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerows(freee_rows)

    print(f"出力完了: {output_file}")
    print("\nプレビュー:")
    for row in freee_rows[:6]:
        print(','.join(row))

if __name__ == '__main__':
    main()
