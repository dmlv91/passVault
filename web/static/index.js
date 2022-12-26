function deleteEntry(entryID) {
    fetch('/delete-entry', {
        method: 'POST',
        body: JSON.stringify({entryID: entryID}),
    }).then((_res) => {
        window.location.href = "/";
    });
};

// function newEntry(newEntry) {
//     fetch('/modal', {
//         method: 'POST',
//         body: JSON.stringify({service: service, username: username, password: password}),
//     }).then((_res) => {
//         window.location.href = "/";
//     });
//     console.log(body)
// }
