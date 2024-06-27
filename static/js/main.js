document.addEventListener('DOMContentLoaded', function () {
    const user_dropdown_btn = document.querySelector('.user_dropdown_btn');
    const user_dropdown = document.querySelector('.user_dropdown');
    const user_dropdown_close = document.querySelector('.user_dropdown_close');

    const lang_form = document.querySelector('#lang_form');
    const lang_selector = document.querySelector('#lang_selector');
    const lang_btns = document.querySelectorAll('#lang_btn');

    const profile_form = document.querySelector('#profile_form');
    const profile_photo_label = document.querySelector('#profile_file')
    const profile_form_btns = document.querySelectorAll('#profile_form button');
    const profile_elements = profile_form?.elements;
    const uploaded_file_box = document.querySelector('#uploaded_file')
    const uploaded_file_path = document.querySelector('#uploaded_file span')
    const uploaded_file_btn = document.querySelector('#uploaded_file div')


    // User dropdown toggle
    if (user_dropdown_btn && user_dropdown && user_dropdown_close) {
        user_dropdown_btn.addEventListener('click', () => {
            user_dropdown.classList.toggle('hidden');
            user_dropdown_close.classList.toggle('hidden');
        });
        user_dropdown_close.addEventListener('click', () => {
            user_dropdown.classList.toggle('hidden');
            user_dropdown_close.classList.toggle('hidden');
        });
    }

    // Language selection and form submission
    if (lang_btns && lang_selector && lang_form) {
        lang_btns.forEach((btn) => {
            btn.addEventListener('click', () => {
                const value = btn.innerText;
                lang_selector.value = value.toLowerCase();
                lang_form.submit();
            });
        });
    }
    // Profile form edit/cancel handling
    if (profile_form && profile_form_btns && profile_elements) {
        profile_form_btns.forEach((btn) => {
            btn.addEventListener('click', (event) => {
                event.preventDefault();
                if (btn.name === 'edit') {
                    profile_form_btns[0].classList.toggle('hidden');
                    profile_form_btns[1].classList.toggle('hidden');
                    profile_form_btns[2].classList.toggle('hidden');
                    profile_photo_label.classList.toggle('hidden');
                    for (let element of profile_elements) {
                        if (element.tagName.toLowerCase() === 'input') {
                            element.removeAttribute('disabled');
                        }
                    }
                } else if (btn.name === 'cancel') {
                    profile_form.reset();
                    profile_form_btns[0].classList.toggle('hidden');
                    profile_form_btns[1].classList.toggle('hidden');
                    profile_form_btns[2].classList.toggle('hidden');
                    profile_photo_label.classList.toggle('hidden');
                    uploaded_file_box.classList.add('hidden')
                    uploaded_file_box.classList.remove('flex')
                    uploaded_file_path.innerText = ""
                    for (let element of profile_elements) {
                        if (element.tagName.toLowerCase() === 'input') {
                            element.setAttribute('disabled', true);
                        }
                    }
                } else {
                    profile_form.submit()
                }
            });
        });

        profile_elements["photo"].addEventListener("change", (event) => {
            uploaded_file_box.classList.remove('hidden')
            uploaded_file_box.classList.add('flex')
            uploaded_file_path.innerText = event.target.value
        })
        console.log(uploaded_file_btn)
        uploaded_file_btn.addEventListener('click', (event) => {
            event.preventDefault()
            profile_elements["photo"].value = ""
            uploaded_file_box.classList.add('hidden')
            uploaded_file_box.classList.remove('flex')
            uploaded_file_path.innerText = ""

        })
    }
});
