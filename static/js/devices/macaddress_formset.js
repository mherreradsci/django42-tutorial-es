// Add more MAC Address formset to device_form.html

const addMoreBtn = document.getElementById("add-more")
const totalNewForms = document.getElementById('id_macaddress_set-TOTAL_FORMS')

addMoreBtn.addEventListener('click', add_new_form)
function add_new_form(event){
    if (event) {
        event.preventDefault()
    }
    const currentMacAddressForms =
        document.getElementsByClassName("macaddress-form")
    const currentFormCount = currentMacAddressForms.length
    const formCopyTarget = document.getElementById("macaddress-form-list")
    const copyEmptyFormElement =
        document.getElementById("empty-form").cloneNode(true)
    copyEmptyFormElement.setAttribute('class', "macaddress-form")
    copyEmptyFormElement.setAttribute('id', `form-${currentFormCount}`)
    const regexp = new RegExp('__prefix__', 'g')
    copyEmptyFormElement.innerHTML =
        copyEmptyFormElement.innerHTML.replace(regexp, currentFormCount)
    totalNewForms.setAttribute('value', currentFormCount + 1)
    formCopyTarget.append(copyEmptyFormElement)
}
