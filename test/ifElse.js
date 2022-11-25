if (time < 10) {
<<<<<<< HEAD
    greeting = "Good" + "jdlskf" + 2;
} else if (time < 20) {
    greeting = 5;
} else if (time) {
    console.log("ok");
} else {
    greeting = 5 + 6 + 2;
}
age = Number(age);
if (isNaN(age)) {
    voteable = true;
} else {
    voteable = null;
}
=======
    greeting = "Good morning";
  } else if (time < 20) {
    greeting = "Good day";
  } else {
    greeting = "Good evening";
  }
  age = Number(age);
  if (isNaN(age)) {
    voteable = "Input is not a number";
  } else {
    voteable = age < 18 ? "Too young" : "Old enough";
  }
>>>>>>> c808dac (chg: testcase)
