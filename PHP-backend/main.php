<?php
$servername = "10.41.143.40:3306";
$username = "phpmyadmin";
$password = "root";
$database = "homeless";


if ($_SERVER['REQUEST_METHOD'] === 'POST') {
  if (!(isset($_POST['name']) && isset($_POST['picture']) && isset($_POST['securityQuestion']) && isset($_POST['securityAnswer']) && isset($_POST['birthDate']))){die("More POST values needed");}
  $conn = mysqli_connect($servername, $username, $password, $database);
  if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
  }
  $name = $_POST["name"];
  $picture = $_POST["picture"];
  $sec_quests = $_POST["securityQuestion"];
  $answers = $_POST["securityAnswer"];
  $birth = $_POST["birthDate"];

  $sql = "INSERT INTO coreData (name, picture, securityQuestion,  securityAnswer, birthDate)
  VALUES ('$name', '$picture', '$sec_quests' , '$answers', '$birth')";

  $conn->query($sql);

  $conn->close();
}

else if ($_SERVER['REQUEST_METHOD'] === 'GET') {
  echo $_GET["name"];
  $name = $_GET["name"];
  $conn = mysqli_connect($servername, $username, $password, $database);
  if ($conn->query($sql) === TRUE) {
    $sql = "SELECT id FROM coreData WHERE name='$name'";
    echo "Success"
  }
  else {
    echo "Error: " . $sql . "<br>" . $conn->error;
  }
  $conn->close();
}
?>
