use std::{io::{BufReader, BufRead, Lines}, fs::File};


fn read_lines<T: AsRef<str>>(path: T) -> Lines<BufReader<File>> {
    let path_str = path.as_ref();
    let file = File::open(path_str).expect(
        format!("Failed to open file '{path_str}'").as_str()
    );
    let reader = BufReader::new(file);
    return reader.lines();
}


fn section_range(section: &str) -> Vec::<i32> {
    return Some(section.split("-").map(|num|
        if let Ok(result) = num.parse::<i32>() {
            return result;
        } else {
            panic!("Unable to parse number");
        }
    )).expect("Failed to parse section").collect();
}


// Does s1 contain s2?
fn does_contain(s1_start: i32, s1_end: i32, s2_start: i32, s2_end: i32) -> bool {
    return s1_start <= s2_start && s1_end >= s2_end;
}


fn overlap_check(section: &str) -> bool {
    let sections: Vec<_> = section.split(",").collect();
    let section_1 = section_range(sections[0]);
    let section_2 = section_range(sections[1]);

    let s1_start = section_1[0];
    let s1_end = section_1[1];

    let s2_start = section_2[0];
    let s2_end = section_2[1];

    return does_contain(s1_start, s1_end, s2_start, s2_end) || does_contain(s2_start, s2_end, s1_start, s1_end);
}


fn main() {
    let count = read_lines("assignments.txt").map(
        |line|
        if let Ok(line_value) = line {
            return overlap_check(&line_value) as i32;
        } else {
            panic!();
        }
    ).sum::<i32>();

    println!("Count: {count}");
}
