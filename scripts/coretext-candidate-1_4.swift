import Foundation
import CoreText
import CoreGraphics
import ImageIO
import UniformTypeIdentifiers

let fontPath = "fonts/JPCS_Engineering_Font_1_4_Candidate.ttf"
let outputPath = "build/coretext-1.4.png"
try FileManager.default.createDirectory(atPath: "build", withIntermediateDirectories: true)
guard let provider = CGDataProvider(url: URL(fileURLWithPath: fontPath) as CFURL),
      let source = CGFont(provider) else { fatalError("Cannot open font") }
let width = 2000, height = 700
let space = CGColorSpaceCreateDeviceRGB()
guard let context = CGContext(data: nil, width: width, height: height, bitsPerComponent: 8,
                              bytesPerRow: width * 4, space: space,
                              bitmapInfo: CGImageAlphaInfo.premultipliedLast.rawValue) else { fatalError("Cannot create image") }
context.setFillColor(CGColor(gray: 1, alpha: 1))
context.fill(CGRect(x: 0, y: 0, width: width, height: height))
let lines: [(String, CGFloat)] = [
    ("/ C4     PART-01 / C4", 36),
    ("/ C4     PART-01 / C4", 56),
    ("C0 C2 C4 C6 C8     E0 E2 E4 E6 E8", 56),
    ("AVATAR   3.14    Lorem ipsum.", 36)
]
for (i, entry) in lines.enumerated() {
    let font = CTFontCreateWithGraphicsFont(source, entry.1, nil, nil)
    let text = NSAttributedString(string: entry.0, attributes: [
        NSAttributedString.Key(kCTFontAttributeName as String): font,
        NSAttributedString.Key(kCTForegroundColorAttributeName as String): CGColor(gray: 0, alpha: 1)
    ])
    let line = CTLineCreateWithAttributedString(text)
    context.textPosition = CGPoint(x: 30, y: height - 100 - i * 125)
    CTLineDraw(line, context)
    if i == 0 { print("\(ISO8601DateFormatter().string(from: Date())) CoreText first-line width \(CTLineGetTypographicBounds(line, nil, nil, nil)) px") }
}
guard let image = context.makeImage(),
      let destination = CGImageDestinationCreateWithURL(URL(fileURLWithPath: outputPath) as CFURL, UTType.png.identifier as CFString, 1, nil) else { fatalError("Cannot write image") }
CGImageDestinationAddImage(destination, image, nil)
if !CGImageDestinationFinalize(destination) { fatalError("Cannot finalize PNG") }
print("\(ISO8601DateFormatter().string(from: Date())) Wrote CoreText proof")
