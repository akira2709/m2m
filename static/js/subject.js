const btn1 = document.getElementById('btn1')
const btn2 = document.getElementById('btn2')
const c = document.getElementById('c')
const back = document.getElementById('btn_back')
const object = document.getElementById('object')
if (Number(c.textContent) === 0){
    btn1.style.color = '#53e3fb'
    btn2.style.color = 'white'
}
if (Number(c.textContent) === 1){
    btn1.style.color = 'white'
    btn2.style.color = '#53e3fb'
}
btn1.onclick = () =>{
    if (Number(c.textContent) === 1){
        let link = document.createElement('a')
        link.href = '/subject/0/' + object.textContent
        document.body.appendChild(link)
        link.click()
        document.body.removeChild(link)
    }
}
btn2.onclick = () =>{
    if (Number(c.textContent) === 0){
        let link = document.createElement('a')
        link.href = '/subject/1/' + object.textContent
        document.body.appendChild(link)
        link.click()
        document.body.removeChild(link)
    }
}
back.onclick = () => {
    let link = document.createElement('a')
    link.href = '/'
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
}