'use strict';

function registerDeleteClicks(doc) {
    const links = document.querySelectorAll('a.delete');
    links.forEach((link) => {
        link.addEventListener('click', (e) => {
            const name = e.target.dataset.name;
            if (confirm(`Möchtest Du den Eintrag «${name}» wirklich löschen?`)) {
                return true;
            } else {
                e.preventDefault();
                return false;
            }
        });
    });
}

registerDeleteClicks(document);
