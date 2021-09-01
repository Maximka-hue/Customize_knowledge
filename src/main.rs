use tokio::fs::File;
use tokio::io::AsyncWriteExt;
use futures::{stream, Stream, StreamExt}; // 0.3.1
use std::{io, path::PathBuf};
use tokio::fs::{self, DirEntry}; // 0.2.4

use pyo3::prelude::*;


fn visit(path: impl Into<PathBuf>) -> impl Stream<Item = io::Result<DirEntry>> + Send + 'static {
    async fn one_level(path: PathBuf, to_visit: &mut Vec<PathBuf>) -> io::Result<Vec<DirEntry>> {
        let mut dir = fs::read_dir(path).await?;
        let mut files = Vec::new();

        while let Some(child) = dir.next_entry().await? {
            if child.metadata().await?.is_dir() {
                to_visit.push(child.path());
            } else {
                files.push(child)
            }
        }

        Ok(files)
    }

    stream::unfold(vec![path.into()], |mut to_visit| {
        async {
            let path = to_visit.pop()?;
            let file_stream = match one_level(path, &mut to_visit).await {
                Ok(files) => stream::iter(files).map(Ok).left_stream(),
                Err(e) => stream::once(async { Err(e) }).right_stream(),
            };

            Some((file_stream, to_visit))
        }
    })
    .flatten()
}

/*
#[tokio::main]
async fn main() {

    let mut file = File::create("LinksCl.txt").await.expect("Create new fle for saving links");
    file.write_all(b"hello, world!").await.expect("Writing in new file");
    println!("Hello, world!");
    let metadata = file.metadata().await.unwrap();
    println!("{:#?}", metadata);
    let root_path =  r"/home/computadormaxim/図書館/ModelingCoding/PracticalProgrammes";
    let paths = visit(root_path);

    paths
        .for_each(|entry| {
            async {
                match entry {
                    Ok(entry) => println!("visiting {:?}", entry),
                    Err(e) => eprintln!("encountered an error: {}", e),
                }
            }
        })
        .await;
    }
    */

    use url::{Url, Position, ParseError};
//#![allow(unused)]
fn main() -> Result<(), ParseError> {

        let parsed = Url::parse("https://github.com/rust-lang/rust/issues?labels=E-easy&state=open")?;
        let cleaned: &str = &parsed[..Position::AfterPath];
        println!("cleaned: {}", cleaned);
        Ok(())
}