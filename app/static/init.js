var formName
var imagesIdsList
window.blog = function (e) {
  if (imagesIdsList.length && window.confirm('Вы уверены?')) {
  } else {
    e.preventDefault()
  }
}

document.addEventListener('DOMContentLoaded', function () {
  try {
    var menu = document.getElementById('menu')

    menu.addEventListener('click', function () {
      if (menu.nextElementSibling.classList.contains('active')) {
        menu.nextElementSibling.classList.remove('active')
      } else {
        menu.nextElementSibling.classList.add('active')
      }
    })
  } catch (e) {}

  try {
    var images = document.getElementById('images').children
    var imagesIds = document.getElementById('images_ids')
    imagesIdsList = []

    if (imagesIds.value) {
      imagesIdsList = imagesIds.value.split(',')
    }

    console.log(imagesIdsList)

    for (var image of images) {
      image.addEventListener('click', function (e) {
        var i = imagesIdsList.indexOf(this.getAttribute('data-id'))

        if (i !== -1) {
          imagesIdsList.splice(i, 1)
          this.children[0].classList.remove('active')
        } else {
          imagesIdsList.push(this.getAttribute('data-id'))
          this.children[0].classList.add('active')
        }

        imagesIds.value = imagesIdsList.join(',')
        console.log(imagesIdsList)
        e.preventDefault()
      })
    }
  } catch (e) {}

  try {
    document.forms['form'].addEventListener('submit', function (e) {
      if (formName) {
        window[formName](e)
      }
    })
  } catch (e) {}

  if (formName === 'blog') {
    var submit = document.forms['form'].submit

    setInterval(function () {
      if (imagesIdsList.length) {
        submit.removeAttribute('disabled')
      } else {
        submit.setAttribute('disabled', 'disabled')
      }
    }, 1000)
  }
})
