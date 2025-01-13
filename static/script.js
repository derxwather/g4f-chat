let чат = document.getElementById('msgs')
let текст = document.getElementById('msg')
let рисунок = document.getElementById('txt')
let картинка = document.getElementById('pic')

function добавить(текст, отЮзера) {
    let блок = document.createElement('div')
    блок.className = отЮзера ? 'msg user' : 'msg bot'
    блок.textContent = текст
    чат.appendChild(блок)
    чат.scrollTop = чат.scrollHeight
}

async function отправить() {
    let сообщение = текст.value.trim()
    if (!сообщение) return
    
    текст.value = ''
    добавить(сообщение, true)
    
    try {
        let ответ = await fetch('/api/chat', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({text: сообщение})
        })
        
        if (!ответ.ok) throw 'не получилось('
        
        let данные = await ответ.json()
        добавить(данные.response)
    } catch (е) {
        console.log('упс:', е)
        добавить('что-то пошло не так 😢')
    }
}

async function нарисовать() {
    let описание = рисунок.value.trim()
    if (!описание) return
    
    рисунок.value = ''
    картинка.style.display = 'none'
    добавить('щас нарисую...', true)
    
    try {
        let ответ = await fetch('/api/generate-image', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({text: описание})
        })
        
        if (!ответ.ok) throw 'не вышло('
        
        let данные = await ответ.json()
        картинка.src = данные.image_url
        картинка.style.display = 'block'
        добавить('держи! 🎨')
    } catch (е) {
        console.log('упс:', е)
        добавить('не получилось нарисовать 😢')
    }
}

текст.addEventListener('keyup', (е) => {
    if (е.key === 'Enter') отправить()
})

рисунок.addEventListener('keyup', (е) => {
    if (е.key === 'Enter') нарисовать()
}) 