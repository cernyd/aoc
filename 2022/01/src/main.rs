// https://adventofcode.com/2022/day/1
use std::fs::File;
use std::io::{self, BufRead};


fn main() {
    let filename = "calories.txt";
    println!("Using file '{filename}'");
    let file = File::open("calories.txt").expect("Failed to open file");
    let reader = io::BufReader::new(file);

    if let Ok(lines) = Ok::<std::io::Lines<io::BufReader<File>>, String>(reader.lines()) {
        for line in lines {
            if let Ok(line_value) = line {
                println!("{line_value}");
            }
        }
    }
}
