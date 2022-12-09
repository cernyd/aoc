use std::{fs::File, io::BufReader, io::{BufRead, Lines}, collections::HashMap, rc::Rc, cell::{RefCell}, borrow::{BorrowMut, Borrow}};


#[derive(Debug)]
struct DirectoryFile {
    name: String,
    size: usize
}


#[derive(Debug)]
struct Directory<'a> {
    parent: Option<&'a mut Box<Directory<'a>>>,
    name: String,
    files: Vec<Box<DirectoryFile>>,
    directories: HashMap::<String, Box<Directory<'a>>>
}


impl<'a> Directory<'a> {
    fn new(parent: Option<&'a mut Box<Directory<'a>>>, name: String) -> Directory {
        return Directory {
            parent: parent,
            name: name,
            files: Vec::new(),
            directories: HashMap::new()
        };
    }
}


#[derive(Debug)]
enum State {
    LoadNext,
    Seek,
    DirEntry,

    ChangeDir,
    ListDir
}


// From day 6
fn read_lines<T: AsRef<str>>(path: T) -> Lines<BufReader<File>> {
    let file = File::open(path.as_ref()).expect("Unable to open file");
    let reader = BufReader::new(file);
    return reader.lines();
}


fn main() {
    let mut state = &State::LoadNext;
    let mut jump_to = &State::Seek;
    let mut lines = read_lines("filesys.txt").map(|line| line.unwrap());

    let mut root_dir = Box::new(Directory::new(None, String::from("/")));
    let mut curdir = &mut root_dir;

    let mut line: String = String::new();
    loop {
        println!("{:?}", curdir);

        match state {
            /* ----------------------------- Load next line ----------------------------- */
            State::LoadNext => {
                let line_value = lines.next();

                if line_value.is_none() {
                    println!("Last line reached, quitting");
                    break;
                }

                line = line_value.unwrap();
                state = jump_to;
            },
            /* ---------------------------- Seek next command --------------------------- */
            State::Seek => {
                if line.starts_with('$') {
                    println!("COMMAND: {line}");
                    match line.split(" ").nth(1).unwrap() {
                        "cd" => {
                            state = &State::ChangeDir;
                        },
                        "ls" => {
                            state = &State::LoadNext;
                            jump_to = &State::ListDir;
                        },
                        _ => ()
                    }
                }
            },
            /* ---------------------------- Change directory ---------------------------- */
            State::ChangeDir => {
                let target_dir = line.split(" ").nth(2).unwrap();
                println!("CD TO '{target_dir}'");

                match target_dir {
                    "/" => {
                        curdir = &mut root_dir;
                    },
                    ".." => {
                        curdir = curdir.parent.as_mut().unwrap();
                        println!("New curdir: '{}'", curdir.name);
                    },
                    _ => {
                        println!("CD to other directory '{}'", target_dir);
                        if !curdir.directories.contains_key(target_dir) {
                            // TODO: parent reference missing
                            let new_dir = Box::new(Directory::new(None, String::from(target_dir)));
                            curdir.directories.insert(
                                String::from(target_dir), new_dir
                            );
                        }

                        curdir = curdir.directories.get_mut(target_dir).unwrap();
                    }
                }

                state = &State::LoadNext;
                jump_to = &State::Seek;
            },
            /* ----------------------------- List directory ----------------------------- */
            State::ListDir => {
                state = &State::LoadNext;
                jump_to = &State::ListDir;

                match line.chars().nth(0).unwrap() {
                    '$' => {
                        state = &State::Seek;
                    },
                    '0'..='9' => {
                        println!("Directory file! {line}");
                    },
                    'd' => {
                        println!("Directory! {line}");
                    },
                    _ => ()
                };
            },
            _ => {
                panic!("Unimplemented state '{state:?}'");
            }
        }
    }
}
