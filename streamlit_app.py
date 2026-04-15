import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Меню", layout="wide")
page = st.sidebar.selectbox(
    "Выбор",
    ["Главная", "Редактор задач", "Обучение модели",
     "Статистика модели", "Сохранение модели",
     "Ученик","Экспорт заданий","runtask","-"]
)

if page == "Главная":
    html_code = """
    <canvas id="bgCanvas"></canvas>
    <style>
    body{margin:0; overflow:hidden; background:#0a0f1f;}
    canvas{position:fixed; top:0; left:0; width:100%; height:100%; z-index:-1;}
    .hero{position:relative; text-align:center; color:white; padding:60px 20px;}
    .hero h1{font-size:56px; background: linear-gradient(90deg,#00d4ff,#0077ff,#00aaff); -webkit-background-clip:text; -webkit-text-fill-color:transparent; margin-bottom:10px; font-weight:bold;}
    .hero p{font-size:20px; color:#a0c4ff; margin-bottom:50px;}
    .grid{display:grid; grid-template-columns: repeat(auto-fit, minmax(220px,1fr)); gap:30px; margin:0 20px 50px 20px;}
    .card{background: linear-gradient(135deg, rgba(0,119,255,0.2), rgba(0,180,255,0.1)); border-radius:20px; padding:40px 20px; text-align:center; transition: transform 0.3s, box-shadow 0.3s; cursor:pointer; border:1px solid rgba(0,180,255,0.3); position:relative;}
    .card:hover{transform: translateY(-10px) rotate(-3deg); box-shadow:0 10px 50px rgba(0,0,0,0.7);}
    .card h2{font-size:22px; margin-bottom:10px; color:#00f0ff;}
    .card p{font-size:16px; color:#a0d4ff;}
    .progress-bar{position:absolute; bottom:10px; left:20px; width:80%; height:8px; background: rgba(255,255,255,0.1); border-radius:4px; overflow:hidden;}
    .progress-bar-inner{height:100%; width:0%; background: linear-gradient(90deg,#00d4ff,#0077ff); border-radius:4px; animation: load 3s forwards;}
    @keyframes load{0%{width:0%;}100%{width:70%;}}
    </style>

    <div class="hero">
        <h1>🎓 AI-педагогика & MML обучение</h1>
        <p>Интерактивная карта Bloom и прогресс учеников</p>
    </div>

    <div class="grid">
        <div class="card"><h2>Знание</h2><p>Факты и определения</p><div class="progress-bar"><div class="progress-bar-inner"></div></div></div>
        <div class="card"><h2>Понимание</h2><p>Смысл и концепции</p><div class="progress-bar"><div class="progress-bar-inner" style="animation-delay:0.3s"></div></div></div>
        <div class="card"><h2>Применение</h2><p>Практические задачи</p><div class="progress-bar"><div class="progress-bar-inner" style="animation-delay:0.6s"></div></div></div>
        <div class="card"><h2>Анализ</h2><p>Разбор информации</p><div class="progress-bar"><div class="progress-bar-inner" style="animation-delay:0.9s"></div></div></div>
        <div class="card"><h2>Синтез</h2><p>Создание нового</p><div class="progress-bar"><div class="progress-bar-inner" style="animation-delay:1.2s"></div></div></div>
        <div class="card"><h2>Оценка</h2><p>Критическая оценка</p><div class="progress-bar"><div class="progress-bar-inner" style="animation-delay:1.5s"></div></div></div>
    </div>

    <script>
    const canvas=document.getElementById('bgCanvas');
    const ctx=canvas.getContext('2d');
    let W=canvas.width=window.innerWidth;
    let H=canvas.height=window.innerHeight;

    // точки сети
    const nodes=[];
    for(let i=0;i<30;i++){
        nodes.push({x:Math.random()*W,y:Math.random()*H,vx:(Math.random()-0.5)*0.5,vy:(Math.random()-0.5)*0.5});
    }

    function draw(){
        ctx.clearRect(0,0,W,H);
        // синусоида
        ctx.beginPath();
        ctx.strokeStyle='rgba(0,200,255,0.3)';
        ctx.lineWidth=2;
        for(let x=0;x<W;x++){ctx.lineTo(x,H/2+50*Math.sin((x+Date.now()*0.002)/50));}
        ctx.stroke();

        // сеть точек и линий
        nodes.forEach(n=>{
            n.x+=n.vx; n.y+=n.vy;
            if(n.x<0||n.x>W)n.vx*=-1;
            if(n.y<0||n.y>H)n.vy*=-1;
            ctx.beginPath();
            ctx.arc(n.x,n.y,3,0,Math.PI*2);
            ctx.fillStyle='rgba(0,255,255,0.8)';
            ctx.shadowColor='rgba(0,255,255,0.8)'; ctx.shadowBlur=10;
            ctx.fill();
            nodes.forEach(o=>{
                let dx=n.x-o.x; let dy=n.y-o.y; let dist=Math.sqrt(dx*dx+dy*dy);
                if(dist<100){ctx.beginPath(); ctx.moveTo(n.x,n.y); ctx.lineTo(o.x,o.y); ctx.strokeStyle='rgba(0,200,255,'+(1-dist/100)*0.3+')'; ctx.lineWidth=1; ctx.stroke();}
            });
        });
        requestAnimationFrame(draw);
    }
    draw();
    window.addEventListener('resize',()=>{W=canvas.width=window.innerWidth; H=canvas.height=window.innerHeight;});
    </script>
    """
    components.html(html_code, height=900, scrolling=True)

# Остальные страницы
elif page == "Редактор задач":
    try:
        import task1
        task1.run()
    except Exception as e:
        st.error(e)
elif page == "Обучение модели": import task2; task2.run()
elif page == "Статистика модели": import task3; task3.run()
elif page == "Сохранение модели": import task4; task4.run()
elif page == "Ученик": import task6; task6.run()
elif page == "Экспорт заданий": import task8; task8.run()
elif page == "runtask": import task_generat; task_generat.run()
elif page == "-": import task9; task9.run()
