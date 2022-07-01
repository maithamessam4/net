function clear_edit_view(postId){
    document.getElementById(`textarea_${postId}`).remove()
    document.getElementById(`save_${postId}`).remove()
 

    document.getElementById(`post_desc_${postId}`).style.display ='block';
    document.getElementById(`edit_${postId}`).style.display ='inline-block';
    document.getElementById(`post_likes_${postId}`).style.display ='block';


}

function update_like(id,likes){
    let like_count = document.getElementById(`post_countlike_${id}`)

    like_count.innerHTML = likes
}

document.addEventListener('DOMContentLoaded', function(){

    document.addEventListener('click' , event =>{
        const element = event.target

        if(element.id.startsWith('post_likeicon_')){

            let id = element.dataset.id

            fetch(`/like_update/${id}` , {
                
                method:"POST",

            })
            .then(function(response) {

                if(response.ok){
                    return response.json()
                }
                else{
                    return Promise.reject('error')
                }
            })
            .then(function(data){

                let likes = data.countlike;
                let likepost = data.postlike;
                let likeicon = document.getElementById(`post_likeicon_${id}`)
                  update_like(id,likes)

                if(likepost){
                    likeicon.className = 'likeicon fa-heart fas'

                }
                else{
                    likeicon.className = 'likeicon fa-heart far'
                }


            })

            .catch(function(er){
                console.log('failing' ,er)
            })
        }

        if(element.id.startsWith('edit_')){

            let editButton = element
            let postId = editButton.dataset.id
            let postText = document.getElementById(`post_desc_${postId}`)

            let textArea = document.createElement('textarea')
            textArea.innerHTML = postText.innerHTML
            textArea.id = `textarea_${postId}`
            textArea.className = `form-control`
            document.getElementById(`post_descgroup_${postId}`).append(textArea)

            postText.style.display = 'none';

            //hiding likes
            document.getElementById(`post_likes_${postId}`).style.display = 'none' 

            editButton.style.display = 'none';



            let saveButton = document.createElement('button')
            saveButton.innerHTML = 'save'
            saveButton.className = 'btn btn-primary '

            saveButton.id = `save_${postId}`

            document.getElementById(`save_buttons_${postId}`).append(saveButton)

         
        
            

            saveButton.addEventListener('click', function(){

                textArea = document.getElementById(`textarea_${postId}`)

                fetch(`/edit_post/${postId}`, {

                    method:'POST',
                    body: JSON.stringify({
                        desc: textArea.value,
                    })
                })

                .then(response => {
                    if(response.ok || response.status == 400){

                        return response.json()
                    }
                    else if (response.status === 404){

                        clear_edit_view(postId)

                        editButton.style.display = 'none';

                        return Promise.reject('error 404')

                    }
                    else{
                        return Promise.reject('there is an an error' + response.status)
                    }
                })

                .then(result => {

                    if(!result.error){
                        postText.innerHTML = result.desc

                        clear_edit_view(postId)
                    }
                    else{

                        clear_edit_view(postId)
                        editButton.style.display = 'none';
                    }
                })
                .catch(error =>{
                    console.error(error)
                })
            })
        }

    })
})