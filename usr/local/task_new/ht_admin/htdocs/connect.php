<?php
header('Content-Type: text/html; charset=utf-8');
if(isset($argv[1])){
    mysql_connect("localhost", "admintask" , "rom724Kz");
    mysql_query("SET NAMES utf8");
    $data = mysql_fetch_assoc(mysql_query("select * from tasks_new.thread where id = '".(int)($argv[1])."'"));
    echo $data['importance'];
}
?>