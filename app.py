offload = df[OFFLOAD_Q].apply(pd.to_numeric, errors="coerce").mean(axis=1)

crit = df[CRIT_Q].apply(pd.to_numeric, errors="coerce").copy()
crit["q15"] = 6 - crit["q15"]
crit_mean = crit.mean(axis=1)

plt.figure(figsize=(6, 4))
plt.bar(
    ["Когнитивная разгрузка", "Критическая верификация"],
    [offload.mean(), crit_mean.mean()],
    color=["#4C72B0", "#55A868"]
)
plt.ylim(0, 5)
plt.ylabel("Средний балл (1–5)")
plt.title("Средние индексы по выборке")
p1 = os.path.join(CHART_DIR, "bar_indices.png")
plt.tight_layout()
plt.savefig(p1)
plt.close()
paths["bar"] = p1

plt.figure(figsize=(6, 4))
plt.scatter(offload, crit_mean, alpha=0.7, color="#C44E52")
plt.xlabel("Когнитивная разгрузка")
plt.ylabel("Критическая верификация")
plt.title("Соотношение индексов")
p2 = os.path.join(CHART_DIR, "scatter.png")
plt.tight_layout()
plt.savefig(p2)
plt.close()
paths["scatter"] = p2

df["_offload"] = offload
df["_crit"] = crit_mean
grp = df.groupby("course")[["_offload", "_crit"]].mean()

plt.figure(figsize=(6, 4))
grp.plot(kind="bar", ax=plt.gca(), color=["#4C72B0", "#55A868"])
plt.ylabel("Средний балл")
plt.title("Индексы по курсам")
plt.xticks(rotation=0)
p3 = os.path.join(CHART_DIR, "by_course.png")
plt.tight_layout()
plt.savefig(p3)
plt.close()
paths["course"] = p3

return paths, offload.mean(), crit_mean.mean()
table_html = df.tail(10).to_html(index=False, border=1)

body = f"""
<h2>Отчёт: получено {n} ответов</h2>
<p><b>Средний индекс когнитивной разгрузки:</b> {off_m:.2f} / 5<br>
<b>Средний индекс критической верификации:</b> {crit_m:.2f} / 5</p>
<h3>Последние 10 ответов</h3>
{table_html}
<p>Диаграммы во вложении.</p>
"""

msg.set_content("Отчёт во вложении (HTML).")
msg.add_alternative(body, subtype="html")

for p in paths.values():
    with open(p, "rb") as f:
        msg.add_attachment(
            f.read(),
            maintype="image",
            subtype="png",
            filename=os.path.basename(p)
        )

ctx = ssl.create_default_context()
with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, context=ctx) as s:
    s.login(SMTP_USER, SMTP_PASS)
    s.send_message(msg)
  try:
            df = pd.read_csv(CSV_PATH)
            paths, off_m, crit_m = make_charts(df)
            send_report(n, df, paths, off_m, crit_m)
        except Exception as e:
            print("Ошибка отчёта:", e)

    return redirect(url_for("thanks"))

return render_template("form.html")
