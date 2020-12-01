<?php
if(isset($_GET['id']) && is_numeric($_GET['id'])){
    @system("/usr/local/bin/php importance.php ".(int)($_GET['id']));
}    

if(isset($argv[1])){
    header('Content-Type: text/html; charset=utf-8');
    mysql_connect("localhost", "admintask" , "rom724Kz");
    mysql_query("SET NAMES utf8");
    $data = mysql_fetch_assoc(mysql_query("select importance from tasks_new.thread where id = '".(int)($argv[1])."'"));
    echo $data['importance'];
}
?>