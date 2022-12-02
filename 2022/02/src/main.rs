use std::io::{self, BufRead};
use std::fs::File;


// Returns an iterator of lines from a target file
fn read_lines(filename: &str) -> std::io::Lines<io::BufReader<File>> {
    let file = File::open(filename).expect(
        &mut format!("Failed to open file '{filename}'").to_string()
    );

    let reader = io::BufReader::new(file);

    return reader.lines();
}


// Returns the score value of a sign
fn shape_value(ch: char) -> i32 {
    return match ch {
        'A' | 'X' => 1,  // Rock
        'B' | 'Y' => 2,  // Paper
        'C' | 'Z' => 3,  // Scissors
        _ => panic!("{}", format!("Unknown value {}", ch).to_string())
    };
}

// Returns true if value B beats value A
fn did_win(a: char, b: char) -> bool {
    return match b {
        'X' =>  // Rock
            a == 'C',  // Beats scissors
        'Y' =>  // Paper
            a == 'A',  // Beats rock
        'Z' =>  // Scissors
            a == 'B',  // Beats paper
        _ => false
    };
}


fn is_draw(a: char, b: char) -> bool {
    return (a == 'A' && b == 'X') || (a == 'B' && b == 'Y') || (a == 'C' && b == 'Z');
}


fn round_score(line: &String) -> i32 {
    assert!(line.len() >= 2);
    let a = line.chars().nth(0).unwrap();
    let b = line.chars().nth(2).unwrap();

    let b_value = shape_value(b);

    let mut score = b_value;

    println!("\n{a} -> {b}");
    println!("{} -> {}", shape_value(a), shape_value(b));
    if did_win(a, b) {
        score += 6;
    } else if is_draw(a, b) {
        score += 3;
    }
    println!("Score: {score}");

    return score;
}


fn main() {
    let filename = "strategy.txt";

    let mut total_score: i32 = 0;
    for (_, line) in read_lines(filename).enumerate() {
        let line_values = line.unwrap();

        let score = round_score(&line_values);
        total_score += score;
    }
    println!("Total score: {total_score}");
}
