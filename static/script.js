'use strict';

function registerDeleteClicks(doc) {
    const links = doc.querySelectorAll('a.delete');
    links.forEach((link) => {
        link.addEventListener('click', (e) => {
            const name = e.target.dataset.name;
            if (!confirm(`Möchtest Du den Eintrag «${name}» wirklich löschen?`)) {
                e.preventDefault();
            }
        });
    });
}

registerDeleteClicks(document);
