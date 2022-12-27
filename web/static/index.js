function deleteEntry(entryID) {
    fetch('/delete-entry', {
        method: 'POST',
        body: JSON.stringify({entryID: entryID}),
    }).then((_res) => {
        window.location.href = "/";
    });
};