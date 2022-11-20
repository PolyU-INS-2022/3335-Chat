CREATE DATABASE ChatRoom;
USE ChatRoom;
create table user(
    ID int NOT NULL AUTO_INCREMENT,
    Name varchar(100),
    password varchar(100),
    email varchar(100),
    constraint user_pkey primary key(ID)
);
create table ChatRecord (
    ID int NOT NULL AUTO_INCREMENT,
    message VARCHAR(200),
    receiver int,
    sender int,
    CreateTime dateTime,
    constraint ChatRecord_pkey primary key(ID),
    constraint ChatRecord_fkey1 foreign key(sender) references user(ID),
    constraint ChatRecord_fkey2 foreign key(receiver) references user(ID)
);
create table Session(
    SessionID VARCHAR(64),
    userID int,
    ExpireTime dateTime,
    constraint Session_pkey primary key(SessionID),
    constraint Session_fkey foreign key(userID) references user(ID)
);
FLUSH PRIVILEGES;
Create user 'session' @'%' identified by 'asbd2&y3sfa31as3^3';
grant ALL PRIVILEGES ON ChatRoom.Session To 'session' @'%';

Create user 'auth' @'%' identified by 'l*G123AS&4Dlasdkj%';
grant ALL PRIVILEGES ON ChatRoom.user To 'auth' @'%';


Create user 'login' @'%' identified by '93yhosag^$YHLHF89qw4gro';
grant select on  ChatRoom.user To 'login' @'%';


Create user 'chatroom' @'%' identified by '7%hgfHS1d124Dlas65T';
grant select,insert on ChatRoom.ChatRecord to 'chatroom'@'%'; 


CREATE EVENT minute_event
ON SCHEDULE every 1 MINUTE
DO
      DELETE from Session WHERE ExpireTime < NOW();