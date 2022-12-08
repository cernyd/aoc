use std::{fs::File, io::BufReader, io::{BufRead, Lines}};


#[derive(Debug)]
struct DirectoryFile {
    name: String,
    size: usize
}


#[derive(Debug)]
struct Directory {
    parent: Option<Box<Directory>>,
    name: String,
    files: Vec<DirectoryFile>,
    directories: Vec<Directory>
}


impl Directory {
    fn new(parent: Option<Directory>, name: String) -> Directory {
        let mut p = None;

        if parent.is_some() {
            p = Some(Box::new(parent.unwrap()));
        }

        return Directory {
            parent: p,
            name: name,
            files: Vec::<DirectoryFile>::new(),
            directories: Vec::<Directory>::new()
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

    let mut root_dir = Directory::new(None, String::from("/"));
    let mut curdir = &root_dir;

    println!("{root_dir:?}");

    let mut line: String = String::new();
    loop {
        match state {
            State::LoadNext => {
                let line_value = lines.next();

                if line_value.is_none() {
                    println!("Last line reached, quitting");
                    break;
                }

                line = line_value.unwrap();
                state = jump_to;
            },
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
            State::ChangeDir => {
                let target_dir = line.split(" ").nth(2).unwrap();
                println!("CD TO '{target_dir}'");

                match target_dir {
                    "/" => {
                        curdir = &root_dir;
                    },
                    ".." => {
                        let dir = curdir.parent.as_ref();

                        if dir.is_none() {
                            panic!("Directory '{}' has no parent directory!", curdir.name);
                        }
                        curdir = dir.unwrap();
                        println!("New curdir: '{}'", curdir.name);
                    },
                    _ => ()
                }

                state = &State::LoadNext;
                jump_to = &State::Seek;
            },
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

