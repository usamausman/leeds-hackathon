<?php
include 'functions.php';
error_reporting(E_ALL);
ini_set('display_errors', 'on');

$servername = "localhost:3306";
$username = "phpmyadmin";
$password = "root";
$database = "homeless";

$conn = mysqli_connect($servername, $username, $password, $database);

if ($_SERVER['REQUEST_METHOD'] === 'POST'){

    if (isset($_POST['finger_status'])){

        $status = $_POST['finger_status'];

        if ($status === "success"){
            $sql = "UPDATE coreData SET state='3' WHERE State='2'";
        }
        else if ($status == "failure"){
            $sql = "UPDATE coreData SET Error=Error + 1 WHERE State='2'";
        }
        $conn->query($sql);
        die("Finger data successfully added");
    }
    if (!(isset($_POST['name']) && isset($_POST['picture']) && isset($_POST['securityQuestion'])
        && isset($_POST['securityAnswer']) && isset($_POST['birthDate']) && isset($_POST['bankBranch']))){
        die("More POST values needed");
    }

    $name = $_POST["name"];
    $picture = $_POST["picture"];
    $sec_quests = $_POST["securityQuestion"];
    $answers = $_POST["securityAnswer"];
    $birth = $_POST["birthDate"];
    $bank = $_POST["bankBranch"];

    $sql = "INSERT INTO coreData (name, picture, securityQuestion,  securityAnswer, birthDate) VALUES ('$name', '$picture', '$sec_quests' , '$answers', '$birth', '$bank')";

    $conn->query($sql);
}

else if ($_SERVER['REQUEST_METHOD'] === 'GET'){
    if (isset($_GET["name"])){

        $name = $_GET["name"];
        $sql = "SELECT id, name FROM coreData WHERE name='$name'";
        $result = $conn->query($sql);

        if ($result->num_rows > 0){
            while ($row = $result->fetch_assoc()){
                if ($row["id"] === ""){
                    $id = getRandomHex(16);
                    $result = $conn->query("UPDATE coreData SET id='$id' WHERE name='$name'");
                    echo $id;
                }
                else {
                    echo $row["id"];
                }
            }
        }
    }
    else if (isset($_GET["id"])){

        $id = $_GET["id"];
        $sql = "SELECT name FROM coreData WHERE id='$id'";
        $result = $conn->query($sql);

        if ($result->num_rows > 0){
            while ($row = $result->fetch_assoc()){
                $sql = "UPDATE coreData SET state='2' WHERE id='$id'";
                $conn->query($sql);
                echo $row["name"];
            }
        }
        else {
            echo 0;
        }
    }
}

$conn->close();

?>
