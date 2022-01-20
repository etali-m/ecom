var updatBtns = document.getElementsByClassName('update-cart')

for(i = 0; i < updatBtns.length; i++){
    updatBtns[i].addEventListener('click', function(){
        var productId = this.dataset.product
        var action = this.dataset.action
        console.log('productId:', productId, 'action:',action)

        console.log('USER:', user)
        if(user === 'AnonymousUser'){
            console.log('Not logged in')
        }else{
            updateUserOrder(productId, action)
        }
    })

} 

function updateUserOrder(productId, action){
    console.log('User is logged in, sending data..')

    var url = '/update_item/'
    fetch(url, {
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken': csrftoken,
        },
        body:JSON.stringify({'productId': productId, 'action':action})
    })
    .then((response) => {
        return response.json
    } )
    .then((data) =>{
        console.log('data:',data)
        location.reload() //this is to make sure that our page relaod after sending data
    } )
}
