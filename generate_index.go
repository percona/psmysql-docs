


package main

import (
        "bufio"
        "fmt"
        "io/fs"
        "log"
        "os"
        "path/filepath"
        "sort"
        "strings"
)

func main() {
 		// --- Instructions on how to run this script ---
        // Save this code to a file named generate_index.go in the root directory
        // Ensure Go is installed on your system.
        // Open your terminal and navigate to the directory containing generate_index.go.
        // Either - Compile the code (optional): `go build generate_index.go`
        // and then run the code: `./generate_index` 
        // Or `go run generate_index.go` to run the Go script without compile.
        // The script generates index-contents.md inside the "docs" directory.
        // --- End of Instructions ---
        docsDir := "docs"
        indexFileName := "index-contents.md"
        indexFilePath := filepath.Join(docsDir, indexFileName)
        maxDepth := 5
        excludeDirs := map[string]struct{}{
                "_static": {}, "assets": {}, "css": {}, "fonts": {}, "js": {},
                "release-notes": {}, filepath.Join("release-notes", "8.0"): {},
        }
        excludeFiles := map[string]struct{}{
                "404.md": {}, indexFileName: {},
        }
        prefixesToStrip := []string{"The ", "Work with "}

        if err := os.Remove(indexFilePath); err == nil {
                fmt.Printf("Deleted existing index file: %s\n", indexFilePath)
        } else if !os.IsNotExist(err) {
                log.Fatalf("Failed to delete existing index file: %v", err)
        }

        var fileEntries []struct {
                sortKey, displayName, relPath string
                indentLevel                     int
        }

        err := filepath.Walk(docsDir, func(path string, info fs.FileInfo, err error) error {
                if err != nil {
                        return err
                }

                relPath, err := filepath.Rel(docsDir, path)
                if err != nil {
                        return err
                }
                relPath = filepath.ToSlash(relPath)

                depth := strings.Count(relPath, "/")
                if depth > maxDepth {
                        if info.IsDir() {
                                return filepath.SkipDir
                        }
                        return nil
                }

                if info.IsDir() {
                        if _, ok := excludeDirs[info.Name()]; ok {
                                return nil
                        }
                        if _, ok := excludeDirs[relPath]; ok {
                                return nil
                        }
                        return nil
                }

                if !strings.HasSuffix(info.Name(), ".md") {
                        return nil
                }

                if _, ok := excludeFiles[info.Name()]; ok {
                        return nil
                }

                dirsInPath := strings.Split(filepath.Dir(relPath), "/")
                for i := range dirsInPath {
                        if _, ok := excludeDirs[strings.Join(dirsInPath[:i+1], "/")]; ok {
                                return nil
                        }
                }

                if contains(dirsInPath, "release-notes") && info.Name() != "release-notes.md" {
                        return nil
                }

                displayName := extractDisplayName(path)
                if displayName == "" {
                        displayName = strings.TrimSuffix(info.Name(), ".md")
                }

                sortKey := stripPrefixes(displayName, prefixesToStrip)
                sortKey = strings.ToLower(sortKey)

                indentLevel := strings.Count(relPath, "/") - 1
                if indentLevel < 0 {
                        indentLevel = 0
                }

                fileEntries = append(fileEntries, struct {
                        sortKey, displayName, relPath string
                        indentLevel                     int
                }{sortKey, displayName, relPath, indentLevel})

                return nil
        })

        if err != nil {
                log.Fatalf("Error walking the docs directory: %v", err)
        }

        sort.Slice(fileEntries, func(i, j int) bool {
                return fileEntries[i].sortKey < fileEntries[j].sortKey
        })

        var content strings.Builder
        content.WriteString("# Index\n\n")

        prevDir := ""
        for _, entry := range fileEntries {
                dir := filepath.Dir(entry.relPath)
                dir = strings.ReplaceAll(dir, "\\", "/")
                if dir == "." {
                        dir = ""
                }

                if dir != prevDir && dir != "" {
                        dirDisplayName := strings.Replace(dir, "release-notes", "Release notes", -1)
                        indentLevel := strings.Count(dirDisplayName, "/")
                        indent := strings.Repeat("  ", indentLevel)
                        content.WriteString(fmt.Sprintf("%s- %s/\n", indent, dirDisplayName))
                }
                prevDir = dir

                indent := strings.Repeat("  ", entry.indentLevel)
                content.WriteString(fmt.Sprintf("%s  - [%s](%s)\n", indent, entry.displayName, entry.relPath))
        }

        if err := os.WriteFile(indexFilePath, []byte(content.String()), 0644); err != nil {
                log.Fatalf("Failed to write index file: %v", err)
        }

        fmt.Printf("Index generated at %s\n", indexFilePath)
}

func stripPrefixes(s string, prefixes []string) string {
        sLower := strings.ToLower(s)
        for _, prefix := range prefixes {
                if strings.HasPrefix(sLower, strings.ToLower(prefix)) {
                        return s[len(prefix):]
                }
        }
        return s
}

func contains(slice []string, item string) bool {
        for _, s := range slice {
                if strings.EqualFold(s, item) {
                        return true
                }
        }
        return false
}

func extractDisplayName(filePath string) string {
        file, err := os.Open(filePath)
        if err != nil {
                fmt.Printf("Error opening file %s: %v\n", filePath, err)
                return ""
        }
        defer file.Close()

        scanner := bufio.NewScanner(file)
        for scanner.Scan() {
                line := strings.TrimSpace(scanner.Text())
                if strings.HasPrefix(line, "# ") {
                        return strings.TrimSpace(line[2:])
                }
        }
        if err := scanner.Err(); err != nil {
                fmt.Printf("Error reading file %s: %v\n", filePath, err)
        }
        return ""
}