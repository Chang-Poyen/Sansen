// Local-only macOS Vision OCR. Original pixels remain authoritative for math.
import Foundation
import Vision
import AppKit

let root = URL(fileURLWithPath: CommandLine.arguments[1])
let files = try FileManager.default.contentsOfDirectory(at: root.appendingPathComponent("slides"), includingPropertiesForKeys: nil).sorted { $0.path < $1.path }
let dest = root.appendingPathComponent("ocr")
try FileManager.default.createDirectory(at: dest, withIntermediateDirectories: true)
let queue = OperationQueue()
queue.maxConcurrentOperationCount = 3
let lock = NSLock()
var completed = 0
for url in files {
    queue.addOperation {
        autoreleasepool {
            let output = dest.appendingPathComponent(url.deletingPathExtension().lastPathComponent + ".json")
            if !FileManager.default.fileExists(atPath: output.path) {
                var record: [String: Any] = ["image": "slides/" + url.lastPathComponent,
                    "engine": "macOS Vision VNRecognizeTextRequest", "math_verified": false,
                    "coordinate_system": "normalized top-left xyxy"]
                do {
                    let request = VNRecognizeTextRequest()
                    request.recognitionLevel = .accurate
                    request.recognitionLanguages = ["en-US"]
                    request.usesLanguageCorrection = false
                    request.minimumTextHeight = 0.005
                    try VNImageRequestHandler(url: url).perform([request])
                    record["status"] = "ok"
                    record["lines"] = (request.results ?? []).compactMap { obs -> [String: Any]? in
                        guard let candidate = obs.topCandidates(1).first else { return nil }
                        let b = obs.boundingBox
                        return ["text": candidate.string, "confidence": candidate.confidence,
                                "bbox": [b.minX, 1-b.maxY, b.maxX, 1-b.minY]]
                    }
                } catch {
                    record["status"] = "error"
                    record["error"] = String(describing: error)
                    record["lines"] = []
                }
                if let data = try? JSONSerialization.data(withJSONObject: record, options: [.prettyPrinted, .sortedKeys]) {
                    try? data.write(to: output, options: .atomic)
                }
            }
            lock.lock()
            completed += 1
            if completed % 50 == 0 { print("OCR \(completed)/\(files.count)"); fflush(stdout) }
            lock.unlock()
        }
    }
}
queue.waitUntilAllOperationsAreFinished()
print("OCR finished: \(completed) images")
