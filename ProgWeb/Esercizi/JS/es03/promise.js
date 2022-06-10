let promise = new Promise((resolve, reject) => {
    setTimeout(() => {
        resolve('Success');
    }, 5000);
}
);

promise.then(
    result => console.log(result),
)