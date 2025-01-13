// Элементы интерфейса
const msgs = document.getElementById('msgs');
const txt = document.getElementById('msg');
const img = document.getElementById('txt');
const pic = document.getElementById('pic');

// Добавляем сообщение в чат
function add(t, u) {
    const m = document.createElement('div');
    m.className = `msg ${u ? 'user' : 'bot'}`;
    m.textContent = t;
    msgs.appendChild(m);
    msgs.scrollTop = msgs.scrollHeight;
}

// Отправляем сообщение
async function send() {
    const t = txt.value.trim();
    if (!t) return;

    // Очищаем ввод
    txt.value = '';
    
    // Показываем сообщение пользователя
    add(t, true);
    
    try {
        // Отправляем запрос
        const r = await fetch('/api/chat', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({text: t})
        });
        
        if (!r.ok) throw 'err';
        
        // Получаем ответ
        const d = await r.json();
        add(d.response);
    } catch (e) {
        console.error(e);
        add('ошибка 😢');
    }
}

// Генерируем картинку
async function gen() {
    const t = img.value.trim();
    if (!t) return;
    
    // Очищаем ввод
    img.value = '';
    
    // Показываем статус
    pic.style.display = 'none';
    add('делаю...', true);
    
    try {
        // Отправляем запрос
        const r = await fetch('/api/generate-image', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({text: t})
        });
        
        if (!r.ok) throw 'err';
        
        // Показываем картинку
        const d = await r.json();
        pic.src = d.image_url;
        pic.style.display = 'block';
        add('готово ��');
    } catch (e) {
        console.error(e);
        add('ошибка 😢');
    }
}

// Обработка Enter
txt.addEventListener('keyup', e => {
    if (e.key === 'Enter') send();
});

img.addEventListener('keyup', e => {
    if (e.key === 'Enter') gen();
}); 