
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(30) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(75) NOT NULL,
  `password` varchar(128) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `last_login` datetime NOT NULL,
  `date_joined` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=MyISAM AUTO_INCREMENT=83 DEFAULT CHARSET=utf8;

CREATE TABLE `aw` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `th_id` int(11) NOT NULL,
  `status` varchar(200) NOT NULL,
  `cr_by_id` int(11) NOT NULL,
  `cr_to_id` int(11) NOT NULL,
  `com` longtext NOT NULL,
  `cr_date` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `aw_cr_by_id` (`cr_by_id`),
  KEY `aw_cr_to_id` (`cr_to_id`)
) ENGINE=MyISAM AUTO_INCREMENT=17 DEFAULT CHARSET=utf8;
CREATE TABLE `awarsuser` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `awarsuser_user_id_id` (`user_id_id`)
) ENGINE=MyISAM AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;
CREATE TABLE `commentfield` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `field_comment_id` int(11) NOT NULL,
  `comment` varchar(200) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `commentfield_field_comment_id` (`field_comment_id`)
) ENGINE=MyISAM AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;
CREATE TABLE `deg1` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `deg1_user_id_id` (`user_id_id`)
) ENGINE=MyISAM AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;
CREATE TABLE `fields` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `type_id` int(11) NOT NULL,
  `field_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fields_type_id` (`type_id`),
  KEY `fields_field_id` (`field_id`)
) ENGINE=MyISAM AUTO_INCREMENT=131 DEFAULT CHARSET=utf8;
CREATE TABLE `instruction` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `type_task_id` int(11) NOT NULL,
  `instruct` longtext NOT NULL,
  PRIMARY KEY (`id`),
  KEY `instruction_type_task_id` (`type_task_id`)
) ENGINE=MyISAM AUTO_INCREMENT=70 DEFAULT CHARSET=utf8;
CREATE TABLE `report` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(200) NOT NULL,
  `link` varchar(30) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
CREATE TABLE `reportsuser` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_report_id` int(11) NOT NULL,
  `report_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `reportsuser_user_report_id` (`user_report_id`),
  KEY `reportsuser_report_id` (`report_id`)
) ENGINE=MyISAM AUTO_INCREMENT=23 DEFAULT CHARSET=utf8;
CREATE TABLE `taskfield` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `weight` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=57 DEFAULT CHARSET=utf8;
CREATE TABLE `tasktype` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  `system_id` tinyint(1) DEFAULT '1',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=80 DEFAULT CHARSET=utf8;
CREATE TABLE `taskuser` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `type_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `taskuser_type_id` (`type_id`),
  KEY `taskuser_user_id` (`user_id`)
) ENGINE=MyISAM AUTO_INCREMENT=1473 DEFAULT CHARSET=utf8;
CREATE TABLE `thread` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `id_global` int(11) NOT NULL,
  `id_local` int(11) NOT NULL,
  `created_by_id` int(11) NOT NULL,
  `deleted_by_id` int(11) DEFAULT NULL,
  `creation_time` time NOT NULL,
  `creation_date` date NOT NULL,
  `deletion_time` datetime DEFAULT NULL,
  `category_id` int(11) NOT NULL,
  `customer_id` int(11) NOT NULL,
  `performer_id` int(11) NOT NULL,
  `finish_date` datetime DEFAULT NULL,
  `importance` varchar(200) NOT NULL,
  `status` varchar(200) NOT NULL,
  `title_id` int(11) NOT NULL,
  `message` longtext NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `thread_id_global` (`id_global`,`id_local`),
  KEY `thread_created_by_id` (`created_by_id`),
  KEY `thread_deleted_by_id` (`deleted_by_id`),
  KEY `thread_category_id` (`category_id`),
  KEY `thread_customer_id` (`customer_id`),
  KEY `thread_performer_id` (`performer_id`),
  KEY `thread_title_id` (`title_id`),
  KEY `thread_status` (`status`)
) ENGINE=MyISAM AUTO_INCREMENT=172286 DEFAULT CHARSET=utf8;
CREATE TABLE `userprofile` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `fio` varchar(100) NOT NULL,
  `office` varchar(100) NOT NULL,
  `post` varchar(100) NOT NULL,
  `telephone_sot` varchar(12) NOT NULL,
  `telephone_work` varchar(6) NOT NULL,
  `telephone_home` varchar(12) NOT NULL,
  `system_id` tinyint(4) NOT NULL DEFAULT '1',
  `login` varchar(30) NOT NULL DEFAULT '',
  `email` varchar(30) NOT NULL DEFAULT '',
  `password` varchar(30) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  UNIQUE KEY `userprofile_user_id` (`user_id`)
) ENGINE=MyISAM AUTO_INCREMENT=82 DEFAULT CHARSET=utf8;
CREATE TABLE `visitedthreads` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `thread_id` int(11) NOT NULL,
  `visited_on` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `visitedthreads_user_id` (`user_id`),
  KEY `visitedthreads_thread_id` (`thread_id`)
) ENGINE=MyISAM AUTO_INCREMENT=174868 DEFAULT CHARSET=utf8;
