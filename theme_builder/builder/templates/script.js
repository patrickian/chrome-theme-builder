const list = document.getElementById('shortcuts-list');
const addBtn = document.getElementById('add-shortcut-btn');
const backdrop = document.getElementById('modal-backdrop');
const modalTitle = document.getElementById('modal-title');
const form = document.getElementById('shortcut-form');
const nameInput = document.getElementById('site-name');
const urlInput = document.getElementById('site-url');
const cancelBtn = document.getElementById('cancel-btn');

let editingIndex = null;

function openModal(index = null, site = { name: '', url: '' }) {
  editingIndex = index;
  modalTitle.textContent = index === null ? 'Add Shortcut' : 'Edit Shortcut';
  nameInput.value = site.name;
  urlInput.value = site.url;
  backdrop.classList.add('open');
  nameInput.focus();
}

function renderShortcuts(shortcuts) {
  list.innerHTML = '';
  shortcuts.forEach((site, index) => {
    const link = document.createElement('a');
    link.className = 'site';
    link.href = site.url;

    const actions = document.createElement('div');
    actions.className = 'action-btns';

    const editBtn = document.createElement('button');
    editBtn.className = 'icon-btn edit-btn';
    editBtn.type = 'button';
    editBtn.title = 'Edit shortcut';
    editBtn.innerHTML = '<svg viewBox="0 0 24 24"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path></svg>';
    editBtn.addEventListener('click', (e) => {
      e.preventDefault();
      e.stopPropagation();
      openModal(index, site);
    });

    const delBtn = document.createElement('button');
    delBtn.className = 'icon-btn delete-btn';
    delBtn.type = 'button';
    delBtn.title = 'Remove shortcut';
    delBtn.innerHTML = '<svg viewBox="0 0 24 24"><polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path></svg>';
    delBtn.addEventListener('click', (e) => {
      e.preventDefault();
      e.stopPropagation();
      const updated = shortcuts.filter((_, i) => i !== index);
      chrome.storage.local.set({ shortcuts: updated }, () => renderShortcuts(updated));
    });

    actions.appendChild(editBtn);
    actions.appendChild(delBtn);

    const iconWrap = document.createElement('div');
    iconWrap.className = 'icon-wrap';
    const img = document.createElement('img');
    const domain = new URL(site.url).hostname;
    img.src = `https://www.google.com/s2/favicons?domain=${domain}&sz=64`;

    const label = document.createElement('span');
    label.className = 'title';
    label.textContent = site.name;

    iconWrap.appendChild(img);
    link.appendChild(iconWrap);
    link.appendChild(label);
    link.appendChild(actions);
    list.appendChild(link);
  });
}

addBtn.addEventListener('click', () => openModal());
chrome.storage.local.get({ shortcuts: [] }, (data) => renderShortcuts(data.shortcuts));

form.addEventListener('submit', (e) => {
  e.preventDefault();
  let url = urlInput.value.trim();
  if (!/^https?:\/\//i.test(url)) url = 'https://' + url;

  const entry = { name: nameInput.value.trim(), url };
  chrome.storage.local.get({ shortcuts: [] }, (data) => {
    const updated = [...data.shortcuts];
    if (editingIndex === null) updated.push(entry);
    else updated[editingIndex] = entry;

    chrome.storage.local.set({ shortcuts: updated }, () => {
      backdrop.classList.remove('open');
      renderShortcuts(updated);
    });
  });
});

cancelBtn.addEventListener('click', () => backdrop.classList.remove('open'));
backdrop.addEventListener('click', (e) => {
  if (e.target === backdrop) backdrop.classList.remove('open');
});
