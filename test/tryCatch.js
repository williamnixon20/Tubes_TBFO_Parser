try {
    let a = 1 + 2;
} catch (error) {
    console.log(error);
} finally {
    console.log("ok");
}

try {
    1 + 2;
} catch (error) {
    console.log("yaa");
}
