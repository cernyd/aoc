use std::{fs::File, io::BufReader, io::{BufRead, Lines}, collections::{HashSet, VecDeque}};


fn read_lines<T: AsRef<str>>(path: T) -> Lines<BufReader<File>> {
    let file = File::open(path.as_ref()).expect("Unable to open file");
    let reader = BufReader::new(file);
    return reader.lines();
}


// Gets index of target character in marker
fn get_index(target: char, marker: &VecDeque::<char>) -> Option<usize> {
    for (i, ch) in marker.iter().enumerate() {
        if *ch == target {
            return Some(i);
        }
    }
    return None;
}


// Finds position of the marker in a `message`, the marker has length of `marker_len`
fn find_marker(message: &String, marker_len: usize) -> Option<usize> {
    let mut marker = VecDeque::<char>::new();

    for (i, ch) in message.chars().enumerate() {
        // If current character somewhere in marker
        if let Some(pos) = get_index(ch, &marker) {
            // Fast forward marker to new possible start
            for _ in 0..=pos {
                marker.pop_front();
            }
        }

        marker.push_back(ch);

        // If marker length achieved
        if marker.len() >= marker_len {
            println!("Found marker after processing {} chars", i+1);
            return Some(i+1);
        }
    }

    return None;
}


fn main() {
    for message in read_lines("message.txt").map(|line| line.unwrap()) {
        println!("{message}");

        // Set marker_len to 4 for part 1, to 14 for part 2
        find_marker(&message, 14);
    }
}
